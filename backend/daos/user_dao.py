from datetime import datetime, timezone
from typing import Optional

from daos.base_pymongo import BasePyMongoDAO

_COLLECTION = "users"


class UserDAO(BasePyMongoDAO):

    def __init__(self):
        from core.database import db
        super().__init__(db[_COLLECTION])

    def find_by_firebase_uid(self, firebase_uid: str) -> Optional[dict]:
        return self.find_one({"firebase_uid": firebase_uid})

    def upsert_by_firebase_uid(self, firebase_uid: str, phone: str) -> dict:
        """Create user on first login; update last_login on subsequent logins."""
        now = datetime.now(timezone.utc)
        return self.find_one_and_upsert(
            filter_query={"firebase_uid": firebase_uid},
            set_data={"phone": phone, "last_login": now},
            set_on_insert_data={"firebase_uid": firebase_uid, "created_at": now},
        )
