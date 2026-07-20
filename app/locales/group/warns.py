# warn actions
ACCESS_RESTRICTED = (
    "🚫 <b>Access Restricted</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "User <b>{first_name}</b> has reached the limit: <code>{warnings}/{max_warns}</code> warnings.\n"
    "Prohibited words: <code>{words}</code>\n\n"
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

# warn_history section
WARN_HISTORY_HEADER = "⚠️ <b>Warn History [{history_scope}]:</b>\n\n"

WARN_NO_RECORDS = "📋 <b>Warn History:</b> <i>No records found.</i>"