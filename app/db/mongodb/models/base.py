# app/db/mongo/models/base.py
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.json_schema import JsonSchemaValue
from typing import Any, Dict

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: JsonSchemaValue, handler
    ) -> Dict[str, Any]:
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def model_dump(self, **kwargs):
        """Convert to dict with proper handling of ObjectId."""
        kwargs.pop("by_alias", None)
        return super().model_dump(by_alias=True, **kwargs)

    class Config:
        populate_by_name = True  # Replaces allow_population_by_field_name
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }