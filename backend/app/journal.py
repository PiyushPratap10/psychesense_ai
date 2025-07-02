from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from datetime import datetime
from typing import List, Optional
from app.schemas import JournalEntryCreate, JournalEntryPublic

class JournalModel:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_entry(self, entry: JournalEntryCreate) -> str:
        entry_data = {
            "title": entry.title,
            "content": entry.content,
            "date": entry.date,
            "created_at": datetime.now(),
            "updated_at": None
        }
        result = await self.collection.insert_one(entry_data)
        return str(result.inserted_id)

    async def get_entries_by_date(self, entry_date) -> List[JournalEntryPublic]:
        cursor = self.collection.find({"date": entry_date})
        entries = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            entries.append(JournalEntryPublic(**doc))
        return entries

    async def update_entry(self, entry_id: str, updated_entry: JournalEntryCreate) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(entry_id)},
            {
                "$set": {
                    "title": updated_entry.title,
                    "content": updated_entry.content,
                    "date": updated_entry.date,
                    "updated_at": datetime.now()
                }
            }
        )
        return result.modified_count == 1

    async def delete_entry(self, entry_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(entry_id)})
        return result.deleted_count == 1
