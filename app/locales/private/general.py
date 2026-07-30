# /start section
WELCOME_TEXT_PRIVATE = (
    "Greetings, <b>{full_name}</b>. I am a specialized <b>Moderation Bot</b> "
    "dedicated to keeping your Telegram communities clean and respectful. 🛡️\n\n"
    "<i>My objective is to monitor and filter prohibited content automatically, "
    "allowing you to focus on meaningful discussions.</i>\n\n"
    "💡 Use the buttons below to explore my features."
)
KB_INFO_BOT = "🛡️ About Bot"
KB_HOW_USE_BOT = "⚙️ Setup Guide"
KB_ALL_COMMANDS = "📜 Commands List"
    
# about
ABOUT_TEXT = (
    "<b>🛡️ Professional Moderation Service</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "I am designed to act as a silent guardian for your chat. By utilizing a modular "
    "architecture and <b>persistent storage</b>, I manage violations in real-time.\n\n"
    "🚀 <b>Core Capabilities:</b>\n"
    "• <b>Join Captcha</b>: Anti-bot verification for new members.\n"
    "• <b>Moderation Logs</b>: Track actions in a dedicated channel.\n"
    "• <b>Centralized Logic</b>: Robust sanctions and history tracking.\n"
    "• <b>Real-time Scanning</b>: Automated filtering of messages and edits.\n"
    "• <b>Anti-Advertising</b>: Automatic removal of external links.\n"
    "• <b>Progressive Bans</b>: Intelligent scaling of restrictions.\n\n"
    "<i>I ensure administrators retain full control while I handle the routine tasks.</i>"
)

# config
CONFIG_TEXT = (
    "<b>⚙️ Configuration Instructions</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "Follow these steps to enable protection:\n\n"
    "1. <b>Add to Group</b>: Invite me to your chat.\n"
    "2. <b>Promote to Admin</b>: Enable <i>Delete Messages</i> and <i>Ban Users</i>.\n"
    "3. <b>Set Log Channel</b>: Use <code>/set_admin_chat</code> in your group.\n"
    "4. <b>Supergroup</b>: Ensure your chat is a supergroup for full features.\n\n"
    "💡 <i>Commands can be used by replying to messages or providing a User ID.</i>"
)



# commands
COMMANDS_TEXT = (
    "<b>📜 Available Commands</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "<b>🛠 Administration:</b>\n"
    "• <code>/set_admin_chat</code> - Set log channel.\n"
    "• <code>/unset_admin_chat</code> - Unset log channel.\n"
    "• <code>/warn</code> - Issue warning (reply).\n"
    "• <code>/unwarn</code> - Remove warning (reply).\n"
    "• <code>/warn_list</code> - View warns history.\n"
    "• <code>/mute</code> - Mute user (reply/ID).\n"
    "• <code>/unmute</code> - Unmute user (reply/ID).\n"
    "• <code>/ban</code> - Ban user (reply/ID).\n"
    "• <code>/unban</code> - Unban user (reply/ID).\n"
    "• <code>/addfilter</code> - Add word to profanity filter.\n"
    "• <code>/removefilter</code> - Remove word from profanity filter.\n"
    "• <code>/mute_list</code> - History of mutes.\n"
    "• <code>/ban_list</code> - History of bans.\n\n"
    "<b>👤 User Commands:</b>\n"
    "• <code>/report</code> - Report violation (reply).\n"
    "• <code>/stats</code> - Your stats or any user's stats (reply).\n"
    "• <code>/help</code> - This menu.\n\n"
    "<b>⏳ Time Formats:</b>\n"
    "<code>10m</code>, <code>1h</code>, <code>1d</code>, <code>1w</code>, <code>permanent</code>\n\n"
    "<b>💡 Usage Note:</b> Admin commands require the bot to have 'Ban Users' privileges."
)
