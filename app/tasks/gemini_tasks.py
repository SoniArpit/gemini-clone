from app.core.celery_app import celery_app
from app.services.gemini import call_gemini_api

@celery_app.task
def generate_reply_task(chatroom_id: str, message: str, user_id: str):
    from app.services.message import save_message_response
    reply = call_gemini_api(message)
    save_message_response(chatroom_id, message, reply, user_id)
    return reply