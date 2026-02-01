from typing import Generic, TypeVar, Optional
from bson import ObjectId

T = TypeVar('T')


class BasePyMongoDAO(Generic[T]):
    def __init__(self, collection):
        self.collection = collection

    def to_object_id(self, id_str: str) -> Optional[ObjectId]:
        try:
            return ObjectId(id_str)
        except Exception:
            return None
        
    def from_object_id(self, obj_id: ObjectId) -> str:
        return str(obj_id)
    
    def generic_serialize(self, document: dict) -> dict:
        #if child class dont want to define serialize use this
        return document
    
    def normalize_id(self, document: dict) -> dict:
        document["id"] = str(document.pop("_id"))
        return document
    
    def serialize(self, document: dict) -> T:
        document = dict(document) # Make a copy to avoid mutating input
        document = self.normalize_id(document)
        return self.generic_serialize(document) # type: ignore
    
    def get_by_id(self, id_str: str) -> Optional[T]:
        obj_id = self.to_object_id(id_str)
        if not obj_id:
            return None
        document = self.collection.find_one({"_id": obj_id})
        if document:
            return self.serialize(document)
        return None
    
    def create(self, data: dict) -> T:
        data.pop("_id", None)  # Ensure no _id is set
        result = self.collection.insert_one(data)
        document = self.collection.find_one({"_id": result.inserted_id})
        return self.serialize(document)
    
    def update(self, id_str: str, data: dict) -> Optional[bool]:
        if any(k.startswith("$") for k in data):
            raise ValueError("Update data must not contain Mongo operators")
        obj_id = self.to_object_id(id_str)
        if not obj_id:
            return None
        result = self.collection.update_one({"_id": obj_id}, {"$set": data})
        if result.matched_count == 0:
            return None
        return result.modified_count > 0
    
    def delete(self, id_str: str) -> bool:
        obj_id = self.to_object_id(id_str)
        if not obj_id:
            return False
        result = self.collection.delete_one({"_id": obj_id})
        return result.deleted_count > 0
    

    def list_filtered_limited_skipped_sorted(
        self,
        filter_query: dict,
        limit: int = 0,
        skip: int = 0,
        sort: Optional[list[tuple[str, int]]] = None
    ) -> list[T]:
        cursor = self.collection.find(filter_query)
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return [self.serialize(doc) for doc in cursor]
