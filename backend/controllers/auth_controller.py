class ProtectedController:
    @staticmethod
    async def dummy_protected():
        return {"message": "Hello World"}