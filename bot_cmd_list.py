from aiogram.types import BotCommand

user_private_commands = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="help", description="How use commands"),
    BotCommand(command="about", description="Information about bot"),
    BotCommand(command="how_use_bot", description="How to use the bot"),
]

admin_group_commands = [
    BotCommand(command="warn", description="Issue a warning (reply required)"),
    BotCommand(command="mute", description="Restrict user (reply or ID required)"),
    BotCommand(command="unmute", description="Lift restriction (reply required)"),
    BotCommand(command="ban", description="Ban user (reply or ID required)"),
    BotCommand(command="unban", description="Unban user (reply or ID required)"),
]
