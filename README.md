# 🛡️ Telegram Profanity Filter & Moderation Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Aiogram-3.x-orange?style=for-the-badge&logo=telegram&logoColor=white" alt="Aiogram Version">
  <img src="https://img.shields.io/badge/Docker-Supported-blue?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Supported">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=header&text=Professional%20Group%20Moderation&fontSize=30" width="100%"/>
</p>

A professional **Telegram moderation tool** built with **Python** and **Aiogram 3**. This bot provides **automatic profanity filtering**, anti-spam protection, and advanced administrative tools to keep your group chats clean and safe. Fully containerized with **Docker Compose**.

---

## 🚀 Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Aiogram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

---

## ✨ Key Features

- **🛡️ Join Captcha**: Automated anti-bot verification for new members.
- **🚀 Automated Moderation**: Real-time scanning for prohibited keywords and external links.
- **🚫 Anti-Advertising**: Automatically detects and removes Telegram invitation links.
- **📊 User Statistics**: Track mutes, bans, warning history, and message count.
- **📜 Moderation Logs**: Dedicated channel logging for all administrative actions.
- **🔧 Modular Architecture**: Decoupled handlers and services for high maintainability.
- **⚠️ Smart Warning System**: Configurable warning limits (default: 5) leading to auto-mutes.
- **📈 Progressive Mutes**: Restriction durations that scale based on violation history.
- **🛠️ Admin Toolkit**: Comprehensive commands for manual moderation and filter management.

---

## 🏗️ Project Architecture

```mermaid
graph TD
    subgraph Core[Bot Entry Point]
        A[app/app.py]
    end

    subgraph Config[Central Configuration]
        CFG[app/config/config.py]
        STR[app/config/strings.py]
        LOG_CFG[app/config/logging_config.py]
    end

    subgraph Handlers[Modular Handlers]
        H_MOD[moderation.py]
        H_CAP[captcha.py]
        H_LST[lists.py]
        H_REP[reports.py]
        H_FADMIN[filter_admin.py]
        H_PRIV[user_private.py]
        H_USR[user.py]
    end

    subgraph Services[Business Logic]
        S_REST[restriction_service.py]
        S_HIST[history_service.py]
        S_LOG[log_service.py]
        S_CAP[captcha_service.py]
        S_FILT[filters_service.py]
    end

    subgraph Data[Persistence & Middlewares]
        DB[(app/database/)]
        MID[app/middlewares/]
        UTL(app/utils/)
    end

    A --> Config
    A --> Handlers
    Handlers --> Services
    Services --> Data
    Handlers --> Data
    A --> MID
```

---

## 📂 File Structure

```text
📦 Telegram-Moderation-Bot
 ┣ 📂 app
 ┃ ┣ 📂 config             # Configuration, strings, and logging setup
 ┃ ┣ 📂 database           # SQLAlchemy models, SQLite, and banwords
 ┃ ┣ 📂 filters            # Admin validation and chat-type filters
 ┃ ┣ 📂 handlers           # Modular routers (Moderation, Captcha, Filters, etc.)
 ┃ ┣ 📂 middlewares        # DB session and Statistics middlewares
 ┃ ┣ 📂 services           # Core business logic (Restrictions, History, Filters)
 ┃ ┣ 📂 utils              # Helper functions (Time parsing, Text normalization)
 ┃ ┣ 📜 app.py             # Main entry point & dispatcher configuration
 ┃ ┣ 📜 requirements.txt   # Project dependencies
 ┃ ┗ 📜 .env               # Environment variables
 ┣ 📜 docker-compose.yml     # Docker orchestration
 ┗ 📜 LICENSE                # MIT License
```

---

## 📋 Available Commands

### 👤 Private Chat
- `/start` — Start the bot and get an overview.
- `/help` — Detailed guide on how to use commands.
- `/stats` — View your personal statistics.
- `/about` — Technical information about the bot.
- `/how_use_bot` — Step-by-step setup instructions.

### 👥 Group Moderation (Admin Only)
- `/set_admin_chat` — Configure current chat for admin logs.
- `/unset_admin_chat` — Disable admin logging for current chat.
- `/warn` — Issue a warning (Reply required).
- `/unwarn` — Remove one warning (Reply required).
- `/mute [duration/ID] [set] [reason]` — Mute a user.
- `/unmute [ID]` — Lift a mute.
- `/ban [duration/ID] [set] [reason]` — Ban a user.
- `/unban [ID]` — Lift a ban.
- `/addfilter [word]` — Add a word to the profanity filter.
- `/removefilter [word]` — Remove a word from the filter.
- `/mute_list [current]` — View mute history.
- `/ban_list [current]` — View ban history.
- `/warn_list` — View warning history.

### 🛡️ Public Group Commands
- `/report` — Report a message to admins (Reply required).
- `/stats` — View your stats in the current chat.

---

## ⚙️ Installation & Setup

### 🐳 Method 1: Docker (Recommended)
1. **Clone the repository**:
   ```bash
   git clone https://github.com/kapusta123b/Telegram-Moderation-Bot
   cd Telegram-Moderation-Bot
   ```
2. **Configure environment**:
   Create `app/.env` and add your token:
   ```env
   BOT_TOKEN=your_bot_token_here
   ```
3. **Launch with Docker Compose**:
   ```bash
   docker-compose up -d --build
   ```

### 🐍 Method 2: Manual Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/kapusta123b/Telegram-Moderation-Bot
   cd Telegram-Moderation-Bot
   ```
2. **Install dependencies**:
   ```bash
   pip install -r app/requirements.txt
   ```
3. **Configure environment**:
   Create `app/.env`:
   ```env
   BOT_TOKEN=your_bot_token_here
   ```
4. **Run the bot**:
   ```bash
   cd app
   python app.py
   ```

---

## ⚠️ Important Note

This bot uses a keyword-matching system. You can manage the filter list directly using `/addfilter` and `/removefilter` commands in your group, or by manually editing `app/database/banwords.txt`.

---

## 🤝 Connect

<p align="center">
  <a href="https://t.me/kapusta123b">
    <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram" />
  </a>
  <a href="mailto:fartuchoknik22@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail" />
  </a>
</p>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=60&section=footer" width="100%"/>
</p>

<p align="center">
  <sub>Made with ❤️ for clean communities</sub>
</p>
