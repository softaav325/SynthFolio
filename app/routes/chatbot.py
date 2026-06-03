from flask import Blueprint, request, jsonify, session
from app.services.ai_service import ai_service
from app.services.rag_service import rag_service
from app.config import SYSTEM_PROMPT
import logging
import time
import html
import requests
# Config logger
logger = logging.getLogger("chatbot_routes")
chatbot_bp = Blueprint('chatbot', __name__)

# Constants
MAX_MESSAGE_LENGTH = 2000
HISTORY_LIMIT = 20  # Save last 20 messenges

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint from AI
    """
    # 1. Security from spam (Rate Limiting)
    current_time = time.time()
    last_request_time = session.get('last_request_time', 0)
    if current_time - last_request_time < 3:  # Min 3 sec
        logger.warning(f"Rate limit exceeded by IP: {request.remote_addr}")
        return jsonify({"error": "Too many requests. Please wait a few seconds."}), 429
    
    session['last_request_time'] = current_time
    session.modified = True

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    # 2. Limit length line
    raw_user_message = data.get('message', '').strip()
    
    if not raw_user_message:
        return jsonify({"error": "Message content cannot be empty"}), 400

    if len(raw_user_message) > MAX_MESSAGE_LENGTH:
        logger.warning(f"Message too long from IP: {request.remote_addr}. Length: {len(raw_user_message)}")
        return jsonify({"error": f"Message too long. Maximum length is {MAX_MESSAGE_LENGTH} characters"}), 413

    # Security from XSS
    user_message = html.escape(raw_user_message)

    # 3. Work with history
    if 'chat_history' not in session:
        session['chat_history'] = []

    history = session['chat_history']
    history.append({"role": "user", "content": user_message})

    try:
        # 4. RAG
        context = rag_service.get_relevant_context(user_message)
        
        rag_system_prompt = f"{SYSTEM_PROMPT}\n\n### CONTEXT FROM KNOWLEDGE BASE:\n{context if context else 'No specific information found in knowledge base.'}\n\n### INSTRUCTIONS:\nUse the provided context to answer the user's question accurately. If the answer is not in the context and you don't know it, politely say that the information is not available in the profile."

        ai_response = ai_service.send_message(history, system_prompt=rag_system_prompt)

        if ai_response['status'] == 'success':
            bot_answer = ai_response['answer']
            
            history.append({"role": "assistant", "content": bot_answer})
            
            if len(history) > HISTORY_LIMIT:
                history = history[-HISTORY_LIMIT:]
            
            session['chat_history'] = history
            session.modified = True

            return jsonify({
                "answer": bot_answer,
                "model": ai_response['model']
            }), 200
        else:
            error_msg = ai_response.get('message', 'AI service error')
            logger.error(f"AI Service Error from IP {request.remote_addr}: {error_msg}")
            return jsonify({"error": "The AI service is currently unavailable. Please try again later."}), 502

    except requests.exceptions.RequestException as re:
        logger.error(f"Network error calling AI service: {str(re)}")
        return jsonify({"error": "Network error. Please check your connection."}), 503
    except Exception as e:
        logger.exception(f"Unexpected critical error in /api/chat from IP {request.remote_addr}: {str(e)}")
        return jsonify({"error": "An internal server error occurred"}), 500

@chatbot_bp.route('/clear', methods=['POST'])
def clear_history():
    """Эндпоинт для очистки истории диалога."""
    session.pop('chat_history', None)
    return jsonify({"status": "success", "message": "Chat history cleared"}), 200
