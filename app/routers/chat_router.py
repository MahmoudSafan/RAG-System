from fastapi import APIRouter, Depends, HTTPException
from controllers.chat_controller import create_chat, add_message_to_chat, get_chat_history, delete_chat
from controllers.auth_controller import get_current_user

router = APIRouter()

@router.post("/chat")
async def create_new_chat(user: dict = Depends(get_current_user)):
    chat_id = await create_chat(str(user.id))
    return {"chat_id": str(chat_id)}

@router.post("/chat/{chat_id}/message")
async def add_chat_message(chat_id: str, content: str, user: dict = Depends(get_current_user)):
    llm_response = await add_message_to_chat(chat_id, content, user.id)
    return {"llm_response": llm_response}

@router.get("/chat/{chat_id}")
async def retrieve_chat_history(chat_id: str, user: dict = Depends(get_current_user)):
    chat = await get_chat_history(chat_id, user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"chat": chat}

@router.delete("/chat/{chat_id}")
async def remove_chat(chat_id: str, user: dict = Depends(get_current_user)):
    deleted_count = await delete_chat(chat_id, user.id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted successfully"}
