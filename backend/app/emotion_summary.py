from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from dotenv import load_dotenv
import os
from huggingface_hub import InferenceClient
from app.database import mongodb  # Make sure you have this in place

# Load secrets
load_dotenv()
client = InferenceClient(api_key=os.getenv("HF-KEY"))

router = APIRouter()

def limit_to_1000_words(text: str) -> str:
    words = text.split()
    return ' '.join(words[:1000])


def generate_emotional_summary_with_chat_model(user_messages: List[str]) -> str:
    prompt = """
You are an emotional analyst AI trained to give friendly and casual emotional reports for users based on their daily messages.
Given the user's messages for the day, summarize their emotional journey, mood swings, and provide a supportive closing note.

User Messages:
""" + "\n".join(f"- {msg}" for msg in user_messages)

    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=[
                {"role": "system", "content": "You are an assistant that generates friendly, supportive emotional summaries of a person's day based on their chat messages."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500,
            top_p=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"


@router.get("/emotion-summary/{user_id}/{date}")
async def get_emotion_summary(user_id: str, date: str):
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    chat_collection = mongodb["user_chats"]
    cursor = chat_collection.find({"user_id": user_id})

    user_messages: List[str] = []

    async for document in cursor:
        for message_pair in document.get("messages", []):
            user_msg = message_pair.get("user_message", {})
            timestamp = user_msg.get("timestamp")

            # Check and convert timestamp
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp)
                except Exception:
                    continue

            if not timestamp or timestamp.date() != target_date.date():
                continue

            message_text = user_msg.get("message", "")
            if message_text:
                user_messages.append(message_text)

    if not user_messages:
        return {
            "message": f"No messages found for user on {date}.",
            "summary": None
        }

    combined_text = limit_to_1000_words(" ".join(user_messages))
    summary = generate_emotional_summary_with_chat_model(user_messages)

    return {
        "date": date,
        "user_id": user_id,
        "total_messages": len(user_messages),
        "summary": summary
    }
