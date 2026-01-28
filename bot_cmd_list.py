from aiogram.types import BotCommand

user_private_commands = [
    BotCommand(command="start", description="Start the bot"),
    BotCommand(command="help", description="How use commands"),
    BotCommand(command="about", description="Information about bot"),
    BotCommand(command="how_use_bot", description="How to use the bot"),
]

admin_group_commands = [
    BotCommand(command="mute", description="Restrict user (reply required)"),
    BotCommand(command="unmute", description="Lift restriction (reply required)"),
]
