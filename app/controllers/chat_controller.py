from models.chat_model import chat_collection, Chat, Message
from utils.embedding_utils import generate_response
from bson import ObjectId

async def create_chat(user_id: str):
    new_chat = Chat(user_id=user_id)
    chat = await chat_collection.insert_one(new_chat.dict())
    chat_id = chat.inserted_id
    return chat_id

async def add_message_to_chat(chat_id: str, content: str, user_id: str):
    user_message = Message(sender="user", content=content)
    await chat_collection.update_one({"_id": ObjectId(chat_id)}, {"$push": {"messages": user_message.dict()}})
    llm_response = generate_response([content])
    response_message = Message(sender="llm", content=llm_response)
    await chat_collection.update_one({"_id": ObjectId(chat_id)}, {"$push": {"messages": response_message.dict()}})
    return llm_response

async def get_chat_history(chat_id: str, user_id: str):
    chat = await chat_collection.find_one({"_id": ObjectId(chat_id)})
    return chat['messages']

async def delete_chat(chat_id: str, user_id: str):
    result = await chat_collection.delete_one({"_id": ObjectId(chat_id)})
    return result.deleted_count
