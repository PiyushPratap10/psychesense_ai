from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.database import get_db  # adjust import based on your structure
from app.models import User      # adjust model import based on your structure

load_dotenv()
client = InferenceClient(api_key=os.getenv("HF-KEY"))

# Fetch user info from database
async def get_user_info(user_id: str, db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(User).filter_by(user_id=user_id))
        db_user = result.scalars().first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
    return {
        "name": db_user.name,
        "gender": db_user.gender,
        "age": db_user.age
    }

# Generate chatbot response using HuggingFace model with user context
async def chatbot_response(user_message, user_id, db: AsyncSession, conversation_history=None):
    user_info = await get_user_info(user_id, db)
    user_context = f"You are talking to a user named {user_info['name']}, a {user_info['age']} year old {user_info['gender']}. You are their emotional support friend. Talk casually, supportively, and be uplifting."

    if conversation_history is None:
        conversation_history = [
            {"role": "system", "content": user_context}
        ]

    conversation_history.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=conversation_history,
            temperature=0.5,
            max_tokens=256,
            top_p=0.7
        )
        model_response = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": model_response})
        return model_response, conversation_history

    except Exception as e:
        return f"Error: {e}", conversation_history
