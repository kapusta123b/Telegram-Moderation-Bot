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

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Aiogram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
</p>

---

## ✨ Key Features

- **🛡️ Join Captcha**: Automated anti-bot verification for new members with a 5-minute timeout and 24-hour ban for failures.
- **🚀 Automated Moderation**: Real-time scanning of messages and edits for prohibited keywords.
- **📜 Moderation Logs**: Dedicated logging system to track all administrative actions in a chosen channel.
- **🧹 System Cleanup**: Automatically removes "user joined" and "user left" system messages for a cleaner chat.
- **💾 Persistent Storage**: SQLite database powered by **SQLAlchemy 2.0** to track violation history.
- **⚠️ Smart Warning System**: Automatically issues warnings to violators (3/3 warnings lead to auto-mute).
- **📈 Progressive Mutes**: Intelligent restriction system that scales based on history (1h -> 2.5h -> 4h -> 24h -> 3d -> 1.5x scaling).
- **🛠️ Admin Toolkit**: Manual `/warn`, `/mute`, and `/ban` commands with custom durations and reasons.
- **🛡️ Admin Immunity**: Full recognition and protection for group administrators.

---

## 📋 Available Commands

### 👤 Private Chat
- `/start` — Start the bot and get an overview.
- `/help` — Detailed guide on how to use the bot.
- `/about` — Information about the bot's features and technical stack.
- `/how_use_bot` — Step-by-step setup instructions.

### 👥 Group Moderation (Admin Only)
- `/admin_chat` — Set the current chat as the **Admin Log Channel**.
- `/warn` — Issue a formal warning (Reply required).
- `/mute [duration/ID] [set]` — Mute a user (Reply or User ID).
- `/unmute` — Restore message permissions (Reply required).
- `/ban [duration/ID] [set]` — Ban a user from the group (Reply or User ID).
- `/unban [ID]` — Lift a ban (Reply or User ID).

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
    end

    subgraph Logic[Request Processing]
        B(handlers/)
        C(filters/)
        F(middlewares/)
        B1[user_group.py]
        B2[user_private.py]
    end

    subgraph Data[Persistence & Assets]
        E(database/)
        D[(banwords.txt)]
        E1[engine.py]
        E2[models.py]
        E3[requests.py]
    end

    A --> CFG
    A --> F
    F --> B
    B --> C
    B --> E
    B --> D
    
    B1 --- B
    B2 --- B
    
    E1 --- E
    E2 --- E
    E3 --- E
    
    %% Dark Professional Theme
    style Core fill:#1a1a1a,stroke:#444,stroke-width:2px,color:#fff
    style Config fill:#3d3d3d,stroke:#666,stroke-width:2px,color:#fff
    style Data fill:#2d2d2d,stroke:#555,stroke-width:2px,color:#fff
    style Logic fill:#252525,stroke:#444,stroke-width:1px,color:#ccc
    style D fill:#333,stroke:#ffd700,stroke-width:2px,color:#ffd700
```

## 📂 File Structure

```text
📦 Telegram-Moderation-Bot
 ┣ 📂 config             # Permissions, commands, and timing settings
 ┣ 📂 database           # SQLAlchemy 2.0 models & async requests
 ┣ 📂 filters            # Custom logic for Admin & Chat-type validation
 ┣ 📂 handlers           # Core logic: Profanity filter, Captcha, Admin tools
 ┣ 📂 middlewares        # DB session injection & update preprocessing
 ┣ 📜 app.py             # Main entry point & polling configuration
 ┣ 📜 requirements.txt   # Project dependencies
 ┗ 📜 .env               # Environment variables (Token)
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
