# ---- user_group.py -----

DURATION_TEXT = "\n<b>Duration:</b> {duration}"

REASON_LOG_TEXT = "\n<b>Reason:</b> {reason}"

# send_log
MODERATION_LOG = (
    "🛡 <b>Moderation Log</b>\n"
    "<b>User:</b> {first_name} (ID: {user_id})\n"
    "<b>Action:</b> {action}"
    "{duration_block}"
    "{reason_block}"
    "\n<b>Chat:</b> {chat_title}"
)

ACCESS_RESTRICTED = (
    "🚫 <b>Access Restricted:</b> User <b>{first_name}</b> has reached "
    "the limit of <b>{warnings}/3 warnings</b>.\n"
    "<i>A {duration} restriction has been applied (Mute #{mute_count}).</i>"
)

ACTION_WARN_TO = (
    "🔘 <b>Action:</b> Warning issued to <b>{first_name}</b>.\n"
    "📊 <b>Total Warnings:</b> {current_warns}/3"
)

NOTICE_REPLY = "⚠️ <b>Notice:</b> This command must be used in a reply."

NOT_REPLY_TO_MESSAGE = "❌ <b>Error:</b> Provide duration or reply to a message."

INVALID_FORMAT = "⚠️ <b>Invalid Format:</b> Use 10m, 1h, 1d or permanent."

REASON_BLOCK = '\n<b>Description:</b> {reason}'

ACTION_USER = (
    "🚫 <b>Action:</b> User <b>{name}</b> {status_text} "
    "<b>{duration_text}</b>."
    "{reason_block}"
)

# mute section
ALREADY_MUTED = "⚠️ <b>Notice:</b> This user is already muted. Use the <code>set</code> argument to update the duration (e.g., <code>/mute 10m set</code>)."

SYSTEM_ERROR_MUTE = "🚨 <b>System Error:</b> Failed to restrict user."

SYSTEM_ERROR_UNMUTE = "🚨 <b>System Error:</b> Failed to lift restriction."

RESTORED_USER_UNMUTE = "✅ <b>Restored:</b> User <b>{first_name}</b> unmuted."

# ban section
ALREADY_BANNED = "⚠️ <b>Notice:</b> This user is already banned. Use the <code>set</code> argument to update the duration (e.g., <code>/ban 10m set</code>)."

SYSTEM_ERROR_BAN = "🚨 <b>System Error:</b> Failed to ban user."

RESTORED_USER_BAN = "✅ <b>Restored:</b> User <b>{name}</b> unbanned."

VALUE_UNBAN_ERROR = "⚠️ <b>Invalid Format:</b> Use numeric User ID."

USER_IS_NOT_BANNED = "ℹ️ <b>Info:</b> User is not banned or is already a member."

SYSTEM_ERROR_UNBAN = "🚨 <b>System Error:</b> Failed to unban user."

# report section
REPORT_SENT = "✅ <b>Report Sent:</b> Administrators have been notified of this violation."

REPORT_NO_REPLY = "⚠️ <b>Notice:</b> This command must be used in a reply."

# ban_history section
BAN_NO_RECORDS = "📋 <b>Ban History:</b> No records found."

BAN_HISTORY_HEADER = (
    "🚫 <b>Ban History ({history_scope}):</b>\n\n"
)

LIST_RECORD = (
    "👤 <b>User:</b> {name} (ID: {user_id})\n"
    "📅 <b>Date:</b> {date}\n"
    "⏳ <b>Duration:</b> {duration}\n"
    "📝 <b>Reason:</b> {reason}\n"
    "-------------------\n"
)

# mute_history section
MUTE_NO_RECORDS = "📋 <b>Mute History:</b> No records found."

MUTE_HISTORY_HEADER = (
    "🔇 <b>Mute History ({history_scope}):</b>\n\n"
)

# warn_history section

WARN_HISTORY_HEADER = (
    "⚠️ <b>Warn History ({history_scope}):</b>\n\n"
)

WARN_NO_RECORDS = "📋 <b>Warn History:</b> No records found."


# set_admin_chat section
SUCCESS_SET_CHAT = "✅ <b>Success:</b> This channel has been set as the <b>Admin Log Channel</b>."

ALREADY_CONFIGURED = "⚠️ <b>Notice:</b> This channel is already configured for logs."

# auto_moderation section
ADMIN_NOTICE = "⚠️ <b>Admin Notice:</b> Please maintain professional language."

SENT_AUTO_WARN = "⚠️ <b>Warning {current_warns}/3:</b> <b>{first_name}</b>, please refrain from using prohibited language in this chat."

# captcha section
VERIFICATION_TEXT = "🤖 <b>Verification:</b> Hello <b>{first_name}</b>, please confirm that you are not a robot to join the conversation!"

VERIFICATION_FAILED = "❌ <b>{first_name}</b> failed verification and has been restricted for 24 hours."

VERIFICATION_SUCCESS = "✅ Verified! Thank you, you can now send messages."

VERIFICATION_NOT_FOR_YOU = "⚠️ This verification is not for you!"

# bot_added_to_chat section
WELCOME_TEXT_GROUP = (
    "🛡 <b>Profanity Filter Bot</b>\n\n"
    "I will automatically monitor this chat for prohibited language. "
    "Users receive warnings, and after <b>3/3</b> warnings, they are restricted for 1 hour.\n\n"
    "<b>Setup:</b>\n"
    "To function properly, I need administrator rights:\n"
    "1. Open Group Settings > <b>Administrators</b>\n"
    "2. Add me as an admin\n"
    "3. Enable <b>Delete Messages</b> and <b>Ban Users</b> permissions\n\n"
    "Use /help in private to see all my features!"
)

# ---- user_private.py ----

# /start section
WELCOME_TEXT_PRIVATE = (
        "Greetings, <b>{full_name}</b>. I am a specialized moderation bot "
        "dedicated to keeping your Telegram communities clean and respectful. 🛡️\n\n"
        "<i>My primary objective is to monitor and filter prohibited content automatically, "
        "allowing you to focus on meaningful discussions.</i>\n\n"
        "Use the buttons below to learn more about my features or how to set me up."
    )

KB_INFO_BOT = "Information about bot..."
KB_HOW_USE_BOT = "How use the bot?"
KB_ALL_COMMANDS = "View all commands"

# about_bot section

ABOUT_TEXT = (
        "<b>🛡️ Professional Moderation Service</b>\n\n"
        "I am designed to act as a silent guardian for your chat. By utilizing a modular "
        "architecture and <b>persistent storage (SQLAlchemy 2.0)</b>, I identify "
        "and manage violations in real-time.\n\n"
        "<b>Core Capabilities:</b>\n"
        "• <i>Join Captcha</i>: Anti-bot verification for new members (5m timeout).\n"
        "• <i>Moderation Logs</i>: Track all actions in a dedicated channel using /admin_chat.\n"
        "• <i>Centralized Services</i>: Robust logic for sanctions, history, and restrictions.\n"
        "• <i>Persistent Tracking</i>: All warnings and mutes are saved in a database.\n"
        "• <i>Real-time Scanning</i>: Automated filtering of messages and edits.\n"
        "• <i>Automated Warning System</i>: (3/3 warnings lead to auto-mute).\n"
        "• <i>Progressive Mutes</i>: Intelligent scaling of restrictions.\n"
        "• <i>Manual Moderation</i>: Admins can use /warn, /mute, or /ban.\n\n"
        "I respect your administrators and ensure they retain full control while I handle "
        "the routine moderation tasks."
    )

CONFIG_TEXT = (
        "<b>⚙️ Configuration Instructions</b>\n\n"
        "Follow these steps to enable protection in your group:\n\n"
        "1. <b>Add the Bot</b> to your group chat.\n"
        "2. <b>Promote to Administrator</b> and ensure <i>Delete Messages</i> and "
        "<i>Ban Users</i> permissions are enabled.\n"
        "3. <b>Set Log Channel</b>: Use <code>/admin_chat</code> in the group where you want to receive logs.\n"
        "4. <b>Supergroup Activation</b>: Confirm your chat is a Supergroup to allow "
        "me to restrict members and use the captcha feature.\n\n"
        "Once configured, you can use commands by <b>replying</b> to messages or by providing a <b>User ID</b>."
    )

COMMANDS_TEXT = (
        "<b>📜 Available Commands</b>\n\n"
        "<b>Group Administration:</b>\n"
        "• /admin_chat - Set the current chat as the Admin Log Channel.\n"
        "• /warn - Issue a formal warning (reply required).\n"
        "• /mute <code>[time/ID] [set]</code> - Mute user (reply or ID required).\n"
        "• /unmute - Unmute user (reply required).\n"
        "• /ban <code>[time/ID] [set]</code> - Ban user (reply or ID required).\n"
        "• /unban <code>[ID]</code> - Unban user (reply or ID required).\n"
        "• /mute_list - View history of mutes (paginated).\n"
        "• /ban_list - View history of bans (paginated).\n\n"
        "<b>User Commands:</b>\n"
        "• /report - Report a violation to admins (reply required).\n\n"
        "<b>Time Formats:</b>\n"
        "<code>10m</code>, <code>1h</code>, <code>1d</code>, <code>1w</code>, <code>permanent</code>\n\n"
        "<b>Arguments:</b>\n"
        "• <code>set</code> - Use this to update or extend the duration for a user who is already restricted.\n\n"
        "<b>Usage Note:</b> Admin commands require the bot to have 'Ban Users' privileges."
    )