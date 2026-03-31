# 🚀 Telegram AI Monitor


An AI-powered Telegram monitoring dashboard that ingests live messages, classifies them using LLMs, and displays insights through a modern web interface.

---

## 🧠 Overview

Telegram AI Monitor is a full-stack application that:

* Captures Telegram messages via webhooks
* Classifies messages using AI (LLMs)
* Stores structured results in a database
* Displays insights in a clean dashboard

### 🎯 Use Cases

* Community moderation
* Crypto/trading signal detection
* Customer support triage
* Workflow automation

---

## ✨ Features

### 🔌 Telegram Integration

* Webhook-based message ingestion
* Supports private chats and groups
* Extracts sender, message text, and metadata

### 🤖 AI Classification

Messages are categorized into:

* Spam
* Important
* Question
* Normal

Each message includes:

* category
* confidence score
* reasoning

---

### 📊 Dashboard (React)

* Real-time message feed
* Category-based filtering
* Stats overview
* Clean SaaS-style UI

---

### 🗄️ Backend API (Flask)

* REST API for messages and stats
* SQLAlchemy ORM
* Easily extendable architecture

---

## 🏗️ Tech Stack

**Backend**

* Flask
* SQLAlchemy
* OpenAI API
* Telegram Bot API

**Frontend**

* React (Vite)
* Axios

**Infrastructure**

* Render (backend)
* Vercel (frontend)

---

## 📦 Project Structure

```
telegram-ai-monitor/
  backend/
    app.py
    config.py
    models.py
    classifier.py
    telegram_service.py

  frontend/
    src/
      components/
      api/
      App.jsx
```

---

## ⚙️ Setup Instructions

### 🔧 Backend Setup

```bash
cd backend

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env`:

```env
DATABASE_URL=sqlite:///messages.db
TELEGRAM_BOT_TOKEN=your_token
WEBHOOK_BASE_URL=https://your-ngrok-or-domain
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
```

Run:

```bash
python app.py
```

---

### 💻 Frontend Setup

```bash
cd frontend

npm install
npm run dev
```

Create `.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:5000
```

---

## 🔗 Telegram Bot Setup

1. Open Telegram → search **BotFather**
2. Run `/newbot`
3. Copy token
4. Add it to `.env`

---

## 🌐 Webhook Setup

If running locally:

```bash
ngrok http 5000
```

Update `.env`:

```env
WEBHOOK_BASE_URL=https://your-ngrok-url
```

Register webhook:

```bash
curl -X POST http://127.0.0.1:5000/telegram/set-webhook
```

---

## 🚀 Deployment

### Backend (Render)

* Root: `backend`
* Build:

```bash
pip install -r requirements.txt
```

* Start:

```bash
gunicorn app:app
```

Set environment variables:

* TELEGRAM_BOT_TOKEN
* OPENAI_API_KEY
* DATABASE_URL
* WEBHOOK_BASE_URL

---

### Frontend (Vercel)

* Root: `frontend`

Set:

```env
VITE_API_BASE_URL=https://your-backend-url
```

---

## 📡 API Endpoints

### `GET /messages`

Fetch messages

### `POST /messages`

Create + classify message

### `GET /stats`

Category counts

### `POST /telegram/webhook`

Telegram updates

---

## 🧪 Example Output

```json
{
  "category": "Spam",
  "reason": "Promotional content with unrealistic claims",
  "confidence": 0.95
}
```

---

## 🔮 Future Improvements

### 🧠 AI Enhancements

* Open-source LLM support (e.g. Ollama, Mistral, LLaMA)
* Model routing (cost vs accuracy)
* Sentiment & toxicity analysis

---

### ⚙️ Architecture

* Background workers (Celery / queues)
* Async processing
* Redis caching

---

### 👥 Multi-Group Support

* Track multiple Telegram groups
* Group-specific dashboards
* Role-based access

---

### 📊 Analytics

* Message trends
* User activity tracking
* Spam rate monitoring

---

### 🔔 Alerts

* Real-time notifications
* Slack / Discord integration
* Email alerts

---

### 🧑‍💼 SaaS Features

* Authentication
* Multi-tenant system
* Subscription billing

---

## ⚠️ Notes

* SQLite is for local dev only
* Use PostgreSQL in production
* Render free tier may sleep


