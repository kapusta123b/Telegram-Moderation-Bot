# 🛡️ Telegram Profanity Filter & Moderation Bot

<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=24&pause=1000&color=F7F7F7&center=true&vCenter=true&width=500&lines=Secure+Your+Community;Automated+Moderation;Profanity+Filtering;Powered+by+Aiogram+3" alt="Typing SVG" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Aiogram-3.x-orange?style=for-the-badge&logo=telegram&logoColor=white" alt="Aiogram Version">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status">
</p>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=header&text=Professional%20Group%20Moderation&fontSize=30" width="100%"/>
</p>

A professional **Telegram moderation tool** built with **Python** and **Aiogram 3**. This bot provides **automatic profanity filtering**, anti-spam protection, and advanced administrative tools to keep your group chats clean and safe.

---

## 🚀 Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Aiogram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
</p>

---

## ✨ Key Features

- **🛡️ Join Captcha**: Automated anti-bot verification for new members with a 5-minute timeout and 1 hour ban for failures.
- **🚀 Automated Moderation**: Modular routers for real-time scanning of messages and **edits** for prohibited keywords and **external links**.
- **🚫 Anti-Advertising**: Automatically detects and removes Telegram invitation links (`t.me/`) to prevent spam.
- **📊 User Statistics**: Public command for users to track their own mutes, bans, and warning history.
- **📜 Moderation Logs**: Dedicated logging system to track all administrative actions. Automatically **forwards violating messages** to the chosen channel as evidence.
- **🔧 Modular Architecture**: Decoupled handlers for captcha, lists, moderation, reports, and system tasks for better maintainability.
- **⚙️ Centralized Services**: Specialized logic layers for restrictions, history management, and automated warnings.
- **🧹 System Cleanup**: Automatically removes "user joined" and "user left" system messages for a cleaner chat.
- **💾 Persistent Storage**: SQLite database powered by **SQLAlchemy 2.0** to track violation history and bot configuration.
- **⚠️ Smart Warning System**: Automatically issues warnings to violators (default: 5/5 warnings lead to auto-mute).
- **📈 Progressive Mutes**: Intelligent restriction system that scales based on history (1h -> 2.5h -> 4h -> 12h -> 1d -> 1.2x scaling).
- **🛠️ Admin Toolkit**: Manual `/warn`, `/mute`, and `/ban` commands with custom durations, reasons, and ID support.

---

## 📋 Available Commands

### 👤 Private Chat
- `/start` — Start the bot and get an overview.
- `/help` — Detailed guide on how to use the bot.
- `/stats` — View your personal statistics across groups.
- `/about` — Information about the bot's features and technical stack.
- `/how_use_bot` — Step-by-step setup instructions.

### 👥 Group Moderation (Admin Only)
- `/set_admin_chat` — Set the current chat as the **Admin Log Channel**.
- `/unset_admin_chat` — Unset the current chat as the **Admin Log Channel**.
- `/warn` — Issue a formal warning (Reply required).
- `/unwarn` — Remove one warning from a user (Reply required).
- `/mute [duration/ID] [set] [reason]` — Mute a user (Reply or User ID).
- `/unmute [ID]` — Restore message permissions (Reply or User ID).
- `/ban [duration/ID] [set] [reason]` — Ban a user from the group (Reply or User ID).
- `/unban [ID]` — Lift a ban (Reply or User ID).
- `/mute_list [current]` — View history of mutes (Paginated).
- `/ban_list [current]` — View history of bans (Paginated).
- `/warn_list` — View history of warns (Paginated).

> **💡 Note:** Use the `current` argument with `/mute_list` or `/ban_list` to see only active restrictions.

### 🛡️ Public Group Commands
- `/report` — Report a message to administrators (Reply required).
- `/stats` — View your personal statistics in the current chat.

> **💡 Time Formats:** `10m`, `1h`, `1d`, `1w`, or `permanent`.

---

## 🏗️ Project Architecture

```mermaid
graph TD
    subgraph Core[Bot Entry Point]
        A[app.py]
    end

    subgraph Config[Central Configuration]
        CFG[config/config.py]
        STR[config/strings.py]
        LOG_CFG[config/logging_config.py]
    end

    subgraph Handlers[Modular Handlers]
        H_MOD[moderation.py]
        H_CAP[captcha.py]
        H_LST[lists.py]
        H_REP[reports.py]
        H_SYS[system.py]
        H_PRIV[user_private.py]
        H_USR[user.py]
    end

    subgraph Services[Business Logic]
        S_REST[restriction_service.py]
        S_HIST[history_service.py]
        S_LOG[log_service.py]
        S_CAP[captcha_service.py]
    end

    subgraph Data[Persistence & Utils]
        DB[(database/)]
        UTL(utils/)
        FLT(filters/)
    end

    A --> Config
    A --> Handlers
    Handlers --> Services
    Services --> Data
    Handlers --> Data
    
    %% Styling
    style Core fill:#1a1a1a,stroke:#444,stroke-width:2px,color:#fff
    style Config fill:#3d3d3d,stroke:#666,stroke-width:2px,color:#fff
    style Handlers fill:#252525,stroke:#444,stroke-width:1px,color:#ccc
    style Services fill:#2d2d2d,stroke:#555,stroke-width:2px,color:#fff
    style Data fill:#333,stroke:#ffd700,stroke-width:2px,color:#ffd700
```

## 📂 File Structure

```text
📦 Telegram-Moderation-Bot
 ┣ 📂 config             # Configuration, strings, and logging setup
 ┣ 📂 database           # SQLAlchemy models, async requests, and banwords
 ┣ 📂 filters            # Admin validation and chat-type filters
 ┣ 📂 handlers           # Modular routers (Moderation, Captcha, Lists, etc.)
 ┣ 📂 middlewares        # DB session injection middleware
 ┣ 📂 services           # Core business logic (Restrictions, History, Logs)
 ┣ 📂 utils              # Helper functions (Time parsing, Text normalization)
 ┣ 📜 app.py             # Main entry point & dispatcher configuration
 ┣ 📜 requirements.txt   # Project dependencies
 ┗ 📜 .env               # Environment variables
```

---

## 🚀 Quick Start

1. **Add the Bot** to your Telegram group.
2. **Promote to Admin** with the following permissions:
   - 🗑️ **Delete Messages**
   - 🚫 **Ban Users**
3. **Upgrade to Supergroup**: Ensure your chat is a supergroup to enable restriction features.

---

## ⚙️ Installation

1. **Clone & Enter**:
   ```bash
   git clone https://github.com/kapusta123b/Telegram-Moderation-Bot
   cd Telegram-Moderation-Bot
   ```
2. **Install**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure**:
   Add your token in .env file:
   ```env
   SECRET_KEY=your_bot_token
   ```
4. **Launch**:
   ```bash
   python app.py
   ```

---

## ⚠️ Important Note

This bot uses a keyword-matching system. To ensure the best performance for your community, regularly update the `database/banwords.txt` file with words specific to your moderation needs.

---

## 🤝 Support & Connect

<p align="center">
  <a href="https://t.me/kapusta123b">
    <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram" />
  </a>
  <a href="https://github.com/kapusta123b/Telegram-Moderation-Bot/stargazers">
    <img src="https://img.shields.io/badge/Star%20Repo-yellow?style=for-the-badge&logo=github&logoColor=white" alt="Star" />
  </a>
</p>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=60&section=footer" width="100%"/>
</p>

<p align="center">
  <sub>Made with ❤️ for clean communities</sub>
</p>
