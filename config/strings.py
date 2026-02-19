# ---- user_group.py -----

DURATION_TEXT = "\n⏳ <b>Duration:</b> <code>{duration}</code>"

REASON_LOG_TEXT = "\n📝 <b>Reason:</b> <i>{reason}</i>"

SYSTEM_ERROR = "🚨 <b>System Error:</b> <i>Something went wrong. Please contact the administrator.</i>"

# send_log
MODERATION_LOG = (
    "🛡 <b>Moderation Log Entry</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "👤 <b>User:</b> {first_name} [<code>{user_id}</code>]\n"
    "🕹 <b>Action:</b> <code>{action}</code>"
    "{duration_block}"
    "{reason_block}\n"
    "📍 <b>Chat:</b> <i>{chat_title}</i>"
)

# warn section
ACCESS_RESTRICTED = (
    "🚫 <b>Access Restricted</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "User <b>{first_name}</b> has reached the limit: <code>{warnings}/{max_warns}</code> warnings.\n\n"
    "⚖️ <i>Applied {duration} restriction (Mute #{mute_count}).</i>"
)

ACTION_WARN_TO = (
    "🔘 <b>Action:</b> Warning issued to <b>{first_name}</b>.\n"
    "📊 <b>Total Warnings:</b> <code>{current_warns}/{max_warns}</code>"
)

ZERO_CURRENT_WARNS = "ℹ️ <b>Info:</b> This user has <i>no active warnings</i>."

ACTION_UNWARN_TO = (
    "🔘 <b>Action:</b> Unwarning issued to <b>{first_name}</b>.\n"
    "📊 <b>Total Warnings:</b> <code>{current_warns}/{max_warns}</code>"
)

NOTICE_REPLY = "⚠️ <b>Notice:</b> This command must be used as a <b>reply</b> to a message."

NOT_REPLY_TO_MESSAGE = "❌ <b>Error:</b> Please provide a duration or <b>reply</b> to a target message."

INVALID_FORMAT = "⚠️ <b>Invalid Format:</b> Please use formats like <code>10m</code>, <code>1h</code>, <code>1d</code>, or <code>permanent</code>."

REASON_BLOCK = "\n📝 <b>Description:</b> <i>{reason}</i>"

ACTION_USER = (
    "🚫 <b>Action:</b> User <b>{name}</b> was <code>{status_text}</code> "
    "<b>{duration_text}</b>."
    "{reason_block}"
)

# mute section
ALREADY_MUTED = (
    "⚠️ <b>Notice:</b> This user is <b>already muted</b>.\n"
    "💡 Use the <code>set</code> argument to update the duration (e.g., <code>/mute 10m set</code>)."
)

SYSTEM_ERROR_MUTE = "🚨 <b>System Error:</b> Failed to apply restriction to the user."

SYSTEM_ERROR_UNMUTE = "🚨 <b>System Error:</b> Failed to lift the user restriction."

RESTORED_USER_UNMUTE = "✅ <b>Restored:</b> User <b>{first_name}</b> has been <b>unmuted</b>."

# ban section
ALREADY_BANNED = (
    "⚠️ <b>Notice:</b> This user is <b>already banned</b>.\n"
    "💡 Use the <code>set</code> argument to update the duration (e.g., <code>/ban 10m set</code>)."
)

SYSTEM_ERROR_BAN = "🚨 <b>System Error:</b> Failed to ban the user."

RESTORED_USER_BAN = "✅ <b>Restored:</b> User <b>{name}</b> has been <b>unbanned</b>."

VALUE_UNBAN_ERROR = "⚠️ <b>Invalid Format:</b> Please provide a numeric <b>User ID</b>."

USER_IS_NOT_BANNED = "ℹ️ <b>Info:</b> User is not banned or is already a member of this chat."

SYSTEM_ERROR_UNBAN = "🚨 <b>System Error:</b> Failed to unban the user."

# report section
REPORT_SENT = (
    "✅ <b>Report Submitted:</b> Administrators have been notified of this violation."
)

REPORT_NO_REPLY = "⚠️ <b>Notice:</b> The <code>/report</code> command must be used as a <b>reply</b>."

# ban_history section
BAN_NO_RECORDS = "📋 <b>Ban History:</b> <i>No records found.</i>"

BAN_HISTORY_HEADER = "🚫 <b>Ban History [{history_scope}]:</b>\n\n"

LIST_RECORD = (
    "👤 <b>User:</b> {name} [<code>{user_id}</code>]\n"
    "📅 <b>Date:</b> <code>{date}</code>\n"
    "⏳ <b>Duration:</b> <code>{duration}</code>\n"
    "📝 <b>Reason:</b> <i>{reason}</i>\n"
    "━━━━━━━━━━━━━━━━━━\n"
)

# mute_history section
MUTE_NO_RECORDS = "📋 <b>Mute History:</b> <i>No records found.</i>"

MUTE_HISTORY_HEADER = "🔇 <b>Mute History [{history_scope}]:</b>\n\n"

# warn_history section
WARN_HISTORY_HEADER = "⚠️ <b>Warn History [{history_scope}]:</b>\n\n"

WARN_NO_RECORDS = "📋 <b>Warn History:</b> <i>No records found.</i>"


# set_admin_chat section
SUCCESS_SET_CHAT = (
    "✅ <b>Success:</b> This channel is now configured as the <b>Admin Log Channel</b>."
)

SUCCESS_UNSET_CHAT = (
    "✅ <b>Success:</b> This channel has been <b>removed</b> from the log configuration."
)

ALREADY_CONFIGURED = "⚠️ <b>Notice:</b> This channel is already configured for logs."

NOT_CONFIGURED = "⚠️ <b>Notice:</b> This channel is not configured for logs."

# auto_moderation section
ADMIN_NOTICE = "👑 <b>Admin Notice:</b> Please set an example by using professional language."

SENT_AUTO_WARN = (
    "⚠️ <b>Warning {current_warns}/{max_warns}:</b>\n"
    "<b>{first_name}</b>, please refrain from using prohibited language in this community."
)

ADS_MESSAGE = "🚫 <b>Notice:</b> Advertising and external links are prohibited in this channel."

# captcha section
VERIFICATION_TEXT = (
    "🤖 <b>Verification Required</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "Hello <b>{first_name}</b>, please confirm that you are not a robot to join the conversation!"
)

VERIFICATION_FAILED = (
    "❌ <b>{first_name}</b> failed verification and has been restricted for <b>24 hours</b>."
)

VERIFICATION_SUCCESS = "✅ Verified! Welcome to the community, you can now send messages."

VERIFICATION_NOT_FOR_YOU = "⚠️ This verification process is not for you!"

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

# user_stats section
STATS_TEXT = (
    "📊 <b>User Statistics</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "👤 <b>User ID:</b> <code>{user_id}</code>\n"
    "✉️ <b>Messages:</b> <code>{count_messages}</code>\n"
    "🔇 <b>Mutes:</b> <code>{count_mutes}</code>\n"
    "🚫 <b>Bans:</b> <code>{count_bans}</code>\n"
    "⚠️ <b>Warnings:</b> <code>{count_warns}</code>\n"
    "📅 <b>Join Date:</b> <i>{join_date}</i>"
)

# ---- user_private.py ----

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

# about_bot section
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
    "• <code>/mute_list</code> - History of mutes.\n"
    "• <code>/ban_list</code> - History of bans.\n\n"
    "<b>👤 User Commands:</b>\n"
    "• <code>/report</code> - Report violation (reply).\n"
    "• <code>/stats</code> - Your personal stats.\n"
    "• <code>/help</code> - This menu.\n\n"
    "<b>⏳ Time Formats:</b>\n"
    "<code>10m</code>, <code>1h</code>, <code>1d</code>, <code>1w</code>, <code>permanent</code>\n\n"
    "<b>💡 Usage Note:</b> Admin commands require the bot to have 'Ban Users' privileges."
)
