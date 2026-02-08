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

- **🛡️ Join Captcha**: Automated anti-bot verification for new members with timed auto-kick.
- **🚀 Automated Moderation**: Real-time scanning of messages and edits for prohibited keywords.
- **💾 Persistent Storage**: SQLite database powered by **SQLAlchemy 2.0** to track violation history.
- **⚠️ Smart Warning System**: Automatically issues warnings to violators (3/3 warnings lead to auto-mute).
- **📈 Progressive Mutes**: Intelligent restriction system that scales based on history.
- **🛠️ Admin Toolkit**: Manual `/warn`, `/mute`, and `/ban` commands with custom durations.
- **🛡️ Admin Immunity**: Full recognition and protection for group administrators.

---

## 📋 Available Commands

### 👤 Private Chat
- `/start` — Start the bot and get an overview.
- `/help` — Detailed guide on how to use the bot.
- `/about` — Information about the bot's features and technical stack.
- `/how_use_bot` — Step-by-step setup instructions.

### 👥 Group Moderation (Admin Only)
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
    subgraph Core[Bot Engine]
        A[app.py]
    end

    subgraph Logic[Logic & Routing]
        B(handlers/)
        C(filters/)
        F(middlewares/)
    end

    subgraph Storage[Data Persistence]
        E(database/)
        D[(banwords.txt)]
    end

    A --> B
    A --> C
    A --> E
    A --> F
    
    B --> B1[user_group.py]
    B --> B2[user_private.py]
    B1 -.-> D
    
    E --> E1[engine.py]
    E --> E2[models.py]
    E --> E3[requests.py]
    
    F --> F1[db.py]
    
    %% Dark Professional Theme
    style Core fill:#1a1a1a,stroke:#444,stroke-width:2px,color:#fff
    style Storage fill:#2d2d2d,stroke:#555,stroke-width:2px,color:#fff
    style Logic fill:#252525,stroke:#444,stroke-width:1px,color:#ccc
    style D fill:#333,stroke:#ffd700,stroke-width:2px,color:#ffd700
    style B1 fill:#222,stroke:#666,color:#fff
    style B2 fill:#222,stroke:#666,color:#fff
    style E1 fill:#222,stroke:#666,color:#fff
    style E2 fill:#222,stroke:#666,color:#fff
    style E3 fill:#222,stroke:#666,color:#fff
    style F1 fill:#222,stroke:#666,color:#fff
```

---

## 📂 File Structure

```text
📦 Telegram-Moderation-Bot
 ┣ 📂 database          # SQLAlchemy 2.0 models & async requests
 ┣ 📂 filters           # Custom logic gates for messages
 ┣ 📂 handlers          # The brain of the bot (Group & Private)
 ┣ 📂 middlewares       # Database session injection
 ┣ 📜 app.py            # Main entry point & polling
 ┗ 📜 bot_cmd_list.py   # Command menu configuration
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

This bot uses a keyword-matching system. To ensure the best performance for your community, regularly update the `handlers/banwords.txt` file with words specific to your moderation needs.

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
