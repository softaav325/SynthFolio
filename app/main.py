from flask import Flask
from dotenv import load_dotenv
import os
from app.routes.main import main_bp
from app.routes.chatbot import chatbot_bp

def create_app():
    # Загрузка переменных окружения
    load_dotenv()

    app = Flask(__name__)

    # Конфигурация
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'

    # Регистрация Blueprint-ов
    app.register_blueprint(main_bp)
    app.register_blueprint(chatbot_bp, url_prefix='/api')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
