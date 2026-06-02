# 🚀 AI Portfolio Website (Flask + OpenRouter)

A modern portfolio website with an integrated AI assistant that showcases the developer's skills, answers questions, and helps collect leads.

## 🛠 Tech Stack
- **Backend**: Python 3.10+, Flask
- **AI**: OpenRouter API (DeepSeek v3 by default)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Infrastructure**: Docker, Docker Compose

---

## 🚀 Quick Start Guide

### 1. Environment Setup (.env)
Create a `.env` file in the project root directory and fill it with the following data:

```env
# OpenRouter API Key (get it at openrouter.ai)
OPENROUTER_API_KEY=your_api_key_here

# AI Model (default: deepseek/deepseek-chat-v3-0324)
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324

# Flask Secret Key for sessions (any random string)
SECRET_KEY=my-super-secret-key-123

# Debug Mode (True or False)
DEBUG=True
```

### 2. Running the Application

#### Option A: Local Run (via venv)
This method is suitable for development and testing.

```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the environment
# For Windows:
venv\Scripts\activate
# For Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app/main.py
```
Once started, the site will be available at: `http://localhost:8000`

#### Option B: Run via Docker (Recommended)
This method provides maximum stability and isolation.

```bash
# 1. Build and start containers in the background
docker-compose up -d --build

# 2 the Check logs (if something isn't working)
docker-compose logs -f
```
Once started, the site will be available at: `http://localhost:80`

---

## 🛠 Main AI Bot Features
- **Dialogue Memory**: The bot remembers the last 20 messages of the current session.
- **Professional Prompt**: The bot is configured to present skills and collect client contacts.
- **Security**: 
  - Rate Limiting (spam protection: 1 request per 3 sec).
  - XSS Protection (input escaping).
  - Message length limit (2000 characters).
- **Clear History**: Ability to reset the chat history via the "Clear Chat" button.

## 📁 Project Structure
- `app/main.py` — Entry point and Flask configuration.
- `app/config.py` — System prompts and bot settings.
- `app/services/ai_service.py` — OpenRouter API integration logic.
- `app/routes/chatbot.py` — Chatbot API endpoints.
- `app/static/` — Styles and JavaScript.
- `app/templates/` — HTML templates (Jinja2).
