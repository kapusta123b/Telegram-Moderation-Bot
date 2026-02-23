from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from config.config import BAD_WORDS_FILE
from config.strings import (
    ADD_FAIL_FILTER_WORD, ADD_FILTER_WORD, ADD_WORD_EXISTS,
    REMOVE_FAIL_FILTER_WORD, REMOVE_FILTER_WORD, REMOVE_WORD_NOT_FOUND,
    FILTER_NO_ARGS
)
from filters.chat_filters import ChatTypeFilter
from filters.group_filters import IsAdmin
from services.filters_service import add_filter_word, remove_filter_word, _word_exists


filter_router = Router()
filter_router.message.filter(ChatTypeFilter(["group", "supergroup"]))


@filter_router.message(Command('addfilter', 'removefilter'), IsAdmin())
async def profanity_filter(message: types.Message, command: CommandObject):
    """
    Handler for adding or removing words from the profanity filter.
    """

    if not command.args:
        await message.reply(FILTER_NO_ARGS)
        return
    
    action = command.command
    word = command.args.strip()

    if action == "addfilter":
        try:
            with open(BAD_WORDS_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if _word_exists(word, lines):
                await message.reply(ADD_WORD_EXISTS.format(word=word))
                return
        except Exception:
            await message.reply(ADD_FAIL_FILTER_WORD)
            return

        if await add_filter_word(word):
            await message.reply(ADD_FILTER_WORD.format(word=word))
        else:
            await message.reply(ADD_FAIL_FILTER_WORD)

    else:
        try:
            with open(BAD_WORDS_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if not _word_exists(word, lines):
                await message.reply(REMOVE_WORD_NOT_FOUND.format(word=word))
                return
        except Exception:
            await message.reply(REMOVE_FAIL_FILTER_WORD)
            return

        if await remove_filter_word(word):
            await message.reply(REMOVE_FILTER_WORD.format(word=word))
        else:
            await message.reply(REMOVE_FAIL_FILTER_WORD)