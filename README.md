# 🛡 Telegram Profanity Filter Bot

A lightweight and effective Telegram bot built on **Aiogram 3** for automatically moderating group chats by filtering prohibited Russian language and managing user behavior.

---

## Features

- **Automated Moderation**: Scans all incoming messages and edits for banned words.
- **Warning System**: Issues warnings (1-2/3) before taking action.
- **Auto-Restriction**: Automatically restricts users from sending messages for 1 hour after 3 violations.
- **Admin Immunity**: Bot acknowledges administrators but does not restrict them.
- **Minimalistic Design**: Clean and professional HTML-formatted responses.

---

## Project Architecture

```text
tg_profanity_bot/
├── filters/
│   └── chat_types.py    # Logic to distinguish between private and group chats
├── handlers/
│   ├── user_group.py    # Core moderation logic and message handlers
│   └── banword.txt      # Text-based database for prohibited words
├── .env                 # Environment variables (Secret Token)
├── app.py               # Main entry point for the bot
└── requirements.txt     # Project dependencies
```

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd tg_profanity_bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory and add your bot token:
   ```env
   SECRET_KEY=your_telegram_bot_token_here
   ```


4. **Run the Bot**:
   ```bash
   python app.py
   ```

---

## How to Add to Group

To enable protection, follow these steps:
1. Add the bot to your Telegram Group.
2. Go to **Group Settings** > **Administrators**.
3. Promote the bot to **Admin**.
4. Enable **Delete Messages** and **Ban Users** permissions.
5. Turn a regular group into a supergroup so the bot can mute violators.
---

## ⚠️ Disclaimer & Accuracy

> [!IMPORTANT]
> **Accuracy Notice**: This bot uses a keyword-matching algorithm and string normalization. While effective, it **may result in false positives** (the "Scunthorpe problem") or miss creatively obscured words.
>
> It is highly recommended to monitor the bot's actions and refine the `banword.txt` list periodically to suit your community's needs.

---

## License

This project is licensed under the MIT License.
