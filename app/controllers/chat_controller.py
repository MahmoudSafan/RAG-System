from models.chat_model import chat_collection, Chat, Message
from utils.embedding_utils import generate_response

def create_chat(user_id: str):
    new_chat = Chat(user_id=user_id)
    chat_id = chat_collection.insert_one(new_chat.dict()).inserted_id
    return chat_id

def add_message_to_chat(chat_id: str, content: str, user_id: str):
    user_message = Message(sender="user", content=content)
    chat_collection.update_one({"_id": chat_id, "user_id": user_id}, {"$push": {"messages": user_message.dict()}})
    llm_response = generate_response([content])
    response_message = Message(sender="llm", content=llm_response)
    chat_collection.update_one({"_id": chat_id}, {"$push": {"messages": response_message.dict()}})
    return llm_response

def get_chat_history(chat_id: str, user_id: str):
    chat = chat_collection.find_one({"_id": chat_id, "user_id": user_id})
    return chat

def delete_chat(chat_id: str, user_id: str):
    result = chat_collection.delete_one({"_id": chat_id, "user_id": user_id})
    return result.deleted_count
