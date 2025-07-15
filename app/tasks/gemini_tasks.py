from app.core.celery_app import celery_app
from app.services.gemini import call_gemini_api

@celery_app.task
def generate_reply_task(chatroom_id: str, prompt: str):
    from app.services.message import save_message_response
    reply = call_gemini_api(prompt)
    save_message_response(chatroom_id, prompt, reply)
    return reply