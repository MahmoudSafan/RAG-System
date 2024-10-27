from bson import ObjectId
from typing import Any

# Helper function to convert ObjectId fields
def convert_object_ids(data: Any):
    if isinstance(data, dict):
        return {key: convert_object_ids(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_object_ids(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data
