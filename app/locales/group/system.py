# system messages
SYSTEM_ERROR = "🚨 <b>System Error:</b> <i>Something went wrong. Please contact the administrator.</i>"
DURATION_TEXT = "\n⏳ <b>Duration:</b> <code>{duration}</code>"
NOTICE_REPLY = "⚠️ <b>Notice:</b> This command must be used as a <b>reply</b> to a message."
NOT_REPLY_TO_MESSAGE = "❌ <b>Error:</b> Please provide a duration or <b>reply</b> to a target message."
INVALID_FORMAT = "⚠️ <b>Invalid Format:</b> Please use formats like <code>10m</code>, <code>1h</code>, <code>1d</code>, or <code>permanent</code>."
REASON_BLOCK = "\n📝 <b>Description:</b> <i>{reason}</i>"
ACTION_USER = (
    "🚫 <b>Action:</b> User <b>{name}</b> was <code>{status_text}</code> "
    "<b>{duration_text}</b>."
    "{reason_block}"
)
# -------------

# logs
REASON_LOG_TEXT = "\n📝 <b>Reason:</b> <i>{reason}</i>"
MODERATION_LOG = (
    "🛡 <b>Moderation Log Entry</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "👤 <b>User:</b> {first_name} [<code>{user_id}</code>]\n"
    "🕹 <b>Action:</b> <code>{action}</code>"
    "{duration_block}"
    "{reason_block}\n"
    "📍 <b>Chat:</b> <i>{chat_title}</i>"
)
LIST_RECORD = (
    "👤 <b>User:</b> {name} [<code>{user_id}</code>]\n"
    "📅 <b>Date:</b> <code>{date}</code>\n"
    "⏳ <b>Duration:</b> <code>{duration}</code>\n"
    "📝 <b>Reason:</b> <i>{reason}</i>\n"
    "━━━━━━━━━━━━━━━━━━\n"
)
# -------------


# set_admin_chat section
SUCCESS_SET_CHAT = (
    "✅ <b>Success:</b> This channel is now configured as the <b>Admin Log Channel</b>."
)
SUCCESS_UNSET_CHAT = (
    "✅ <b>Success:</b> This channel has been <b>removed</b> from the log configuration."
)
ALREADY_CONFIGURED = "⚠️ <b>Notice:</b> This channel is already configured for logs."
NOT_CONFIGURED = "⚠️ <b>Notice:</b> This channel is not configured for logs."
# -------------


# auto moderation
ADMIN_NOTICE = "👑 <b>Admin Notice:</b> Please set an example by using professional language."
SENT_AUTO_WARN = (
    "⚠️ <b>Warning {current_warns}/{max_warns}:</b>\n"
    "<b>{first_name}</b>, please refrain from using prohibited language in this community.\n"
    "Prohibited word: <code>{words}</code>"
)
ADS_MESSAGE = "🚫 <b>Notice:</b> Advertising and external links are prohibited in this channel."
# -------------

# bot_added_to_chat section
WELCOME_TEXT_GROUP = (
    "🛡 <b>Guardian Moderation Active</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "I will automatically monitor this chat for prohibited language and spam.\n\n"
    "⚖️ Users receive warnings, and after <b>{max_warns}</b> violations, they are restricted.\n\n"
    "⚙️ <b>Setup Requirements:</b>\n"
    "1. Open Group Settings > <b>Administrators</b>\n"
    "2. Add me as an admin\n"
    "3. Enable <b>Delete Messages</b> and <b>Ban Users</b> permissions\n\n"
    "<i>Use /help in private to see all my features!</i>"
)
# -------------


# user section
STATS_TEXT = (
    "📊 <b>User Statistics</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "👤 <b>User name</b>: {user_fullname}\n"
    "🆔 <b>User ID:</b> <code>{user_id}</code>\n"
    "✉️ <b>Messages:</b> <code>{count_messages}</code>\n"
    "🔇 <b>Mutes:</b> <code>{count_mutes}</code>\n"
    "🚫 <b>Bans:</b> <code>{count_bans}</code>\n"
    "⚠️ <b>Warnings:</b> <code>{count_warns}</code>\n"
    "📅 <b>Join Date:</b> <i>{join_date}</i>"
)
# -------------