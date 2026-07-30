# Telegram Moderation Bot

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![Aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0.svg)
![Docker](https://img.shields.io/badge/docker-supported-2496ED.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Telegram bot for group moderation built with Python and Aiogram 3.

## Features

- Profanity filter
- Telegram invite link detection
- Warning system
- Auto mute after warning limit
- Progressive mute durations
- Join captcha
- Moderation logs
- User statistics
- Admin moderation commands
- Modular project structure

---

## Stack

- Python 3.10+
- Aiogram 3
- SQLAlchemy
- SQLite
- Docker / Docker Compose

---

## Project Structure

```text
📦 Telegram-Moderation-Bot
 ┣ 📂 app
 ┃ ┣ 📂 config             # App configuration, logging setup
 ┃ ┣ 📂 locales            # UI text resources, message templates, and localization
 ┃ ┃ ┣ 📂 group            # Group chat messages (bans, mutes, warns, captcha)
 ┃ ┃ ┗ 📂 private          # Private chat messages (main menu, help, user stats)
 ┃ ┣ 📂 database           # SQLAlchemy models, SQLite, and banwords
 ┃ ┣ 📂 filters            # Admin validation and chat-type filters
 ┃ ┣ 📂 handlers           # Modular routers (Moderation, Captcha, Filters, etc.)
 ┃ ┣ 📂 middlewares        # DB session and Statistics middlewares
 ┃ ┣ 📂 services           # Core business logic (Restrictions, History, Filters)
 ┃ ┣ 📂 utils              # Helper functions (Time parsing, Text normalization)
 ┃ ┣ 📜 app.py             # Main entry point & dispatcher configuration
 ┃ ┣ 📜 requirements.txt   # Project dependencies
 ┣ 📜 .env                   # Environment variables
 ┣ 📜 docker-compose.yml     # Docker orchestration
 ┗ 📜 LICENSE                # MIT License
```

---

# Commands

## Private Chat

| Command | Description |
|---|---|
| `/start` | Start bot |
| `/help` | Show help |
| `/stats` | Show personal statistics |
| `/about` | Show project information |
| `/how_use_bot` | Show setup instructions |

---

## Admin Commands

| Command | Description |
|---|---|
| `/set_admin_chat` | Set moderation log chat |
| `/unset_admin_chat` | Disable moderation logs |
| `/warn` | Add warning |
| `/unwarn` | Remove warning |
| `/mute` | Mute user |
| `/unmute` | Remove mute |
| `/ban` | Ban user |
| `/unban` | Remove ban |
| `/addfilter` | Add banned word |
| `/removefilter` | Remove banned word |
| `/mute_list` | Show mute history |
| `/ban_list` | Show ban history |
| `/warn_list` | Show warning history |

### Examples

```text
/warn
/mute 30m spam
/ban 7d advertising
/addfilter badword
```

---

## Public Commands

| Command | Description |
|---|---|
| `/report` | Report message to admins |
| `/stats` | Show user statistics |

---

# Installation

## Docker

Clone repository:

```bash
git clone https://github.com/kapusta123b/Telegram-Moderation-Bot
cd Telegram-Moderation-Bot
```

Edit `.env`:

```env
BOT_TOKEN=your_bot_token
```

Run container:

```bash
docker compose up -d --build
```

Stop container:

```bash
docker compose down
```

---

## Manual Installation

Clone repository:

```bash
git clone https://github.com/kapusta123b/Telegram-Moderation-Bot
cd Telegram-Moderation-Bot
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r app/requirements.txt
```

Edit `.env`:

```env
BOT_TOKEN=your_bot_token
```

Run bot:

```bash
cd app
python app.py
```

---

# Notes

Filter words are stored in:

```text
app/database/banwords.txt
```

You can also manage filters directly from Telegram using:

```text
/addfilter
/removefilter
```
