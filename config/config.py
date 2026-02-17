from datetime import timedelta

from aiogram import types
from aiogram.types import BotCommand

permissions_mute = types.ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
)

permissions_unmute = types.ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

DEFAULT_MUTE_TIME = {
    1: timedelta(hours=1),
    2: timedelta(hours=2.5),
    3: timedelta(hours=4),
    4: timedelta(hours=24),
    5: timedelta(days=3),
}

BAD_WORDS_FILE = "database/banwords.txt"

user_private_commands = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="help", description="How use commands"),
    BotCommand(command="about", description="Information about bot"),
    BotCommand(command="how_use_bot", description="How to use the bot"),
]

admin_group_commands = [
    BotCommand(
        command="admin_chat",
        description="Set the current chat as the Admin Log Channel",
    ),
    BotCommand(command="warn", description="Issue a warning (reply required)"),
    BotCommand(command="mute", description="Restrict user (reply or ID required)"),
    BotCommand(command="unmute", description="Lift restriction (reply required)"),
    BotCommand(command="ban", description="Ban user (reply or ID required)"),
    BotCommand(command="unban", description="Unban user (reply or ID required)"),
    BotCommand(
        command="report", description="Report a violation to admins (reply required)"
    ),
    BotCommand(command="mute_list", description="View history of mutes"),
    BotCommand(command="ban_list", description="View history of bans"),
]


ALLOWED_UPDATES = [
    "message",
    "edited_message",
    "my_chat_member",
    "chat_member",
    "callback_query",
]

# change it if you want more/less warnings before muting the user
MAX_WARNS = 5


DB_URL = "sqlite+aiosqlite:///db.sqlite3"