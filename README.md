# 🤖 Telegram CV Generator Bot

A Telegram bot that collects user information through a guided conversation and generates a professional **PDF CV** automatically — with AI-written descriptions powered by **Groq (Llama 3.3)**.

---

## ✨ Features

- 📋 **Step-by-step conversation flow** — asks users one question at a time
- 🤖 **AI-generated descriptions** — professional summary and experience bullets written automatically via Groq API
- 📄 **PDF output** — clean, professional chronological CV sent directly in Telegram chat
- 👥 **Multi-user support** — handles multiple users simultaneously with isolated in-memory sessions
- 🔒 **Privacy-first** — zero data stored, all session data wiped after PDF is delivered
- ✅ **Input validation** — guards against empty or oversized inputs
- 📊 **Progress indicator** — users always know which question they're on (e.g. `[3/11]`)

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Bot Framework | [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v20+ |
| AI API | [Groq](https://console.groq.com) — `llama-3.3-70b-versatile` |
| PDF Generation | [WeasyPrint](https://weasyprint.org) |
| HTML Templating | [Jinja2](https://jinja.palletsprojects.com) |
| Config | [python-dotenv](https://github.com/theskumar/python-dotenv) |

---

## 📁 Project Structure

```
telegram-cv-bot/
├── bot.py                  # Main bot logic and conversation flow
├── sessions.py             # In-memory session management
├── cv_fields.py            # CV field definitions (user vs AI-generated)
├── ai_writer.py            # Groq API integration
├── pdf_generator.py        # HTML → PDF generation
├── templates/
│   └── cv_template.html    # CV HTML template (Jinja2)
├── .env                    # API keys (never committed)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/ichheisseyazid/telegram-cv-bot.git
cd telegram-cv-bot
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GROQ_API_KEY=your_groq_api_key_here
```

- Get your **Telegram bot token** from [@BotFather](https://t.me/BotFather)
- Get your **Groq API key** (free) from [console.groq.com](https://console.groq.com)

### 5. Run the bot

```bash
python bot.py
```

---

## 🚀 Usage

| Command | Description |
|---|---|
| `/start` | Welcome message |
| `/generate` | Start building your CV |
| `/cancel` | Stop and clear current session |
| `/help` | Show all available commands |

### How it works

1. User sends `/generate`
2. Bot asks questions one by one (name, email, job title, experience, education, skills, etc.)
3. AI silently generates professional descriptions for summary and experience fields
4. Bot renders a styled HTML template and converts it to PDF
5. PDF is sent directly to the user in chat
6. All session data is permanently wiped

---

## 🔒 Privacy

This bot stores **no user data whatsoever**. All information collected during a session lives exclusively in server memory and is deleted the moment the PDF is delivered. No database, no logs, no persistence.

---

## 📦 Requirements

See `requirements.txt`. Main dependencies:

```
python-telegram-bot[job-queue]
groq
weasyprint
jinja2
python-dotenv
```

---

## 🗺️ Roadmap

- [x] Chronological CV type
- [ ] Functional CV type
- [ ] Hybrid CV type
- [ ] Multiple experience entries
- [ ] Profile photo support
- [ ] CV type selection menu
- [ ] Multiple language support

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
