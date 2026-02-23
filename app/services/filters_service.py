import re
from config.config import BAD_WORDS_FILE


def _extract_word(line: str) -> str:
    """
    Normalize a word by removing special characters and converting to lowercase.
    """

    stripped = line.strip()
    word = re.sub(r"[^а-яa-z0-9]", "", stripped.lower())
    return word


def _word_exists(target_word: str, lines: list) -> bool:
    """
    Check if a word exists in the bad words list, ignoring special characters and formatting.
    """

    target = _extract_word(target_word)
    for line in lines:
        if _extract_word(line) == target:
            return True
        
    return False


async def add_filter_word(word: str) -> bool:
    """
    Add a new word to the profanity filter list.
    """

    try:
        with open(BAD_WORDS_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if _word_exists(word, lines):
            return False

        with open(BAD_WORDS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        with open(BAD_WORDS_FILE, 'w', encoding='utf-8') as f:
            f.write(word.lower() + '\n' + content)

        return True
    
    except Exception:
        return False
    

async def remove_filter_word(word: str) -> bool:
    """
    Remove a word from the profanity filter list.
    """

    try:
        with open(BAD_WORDS_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if not _word_exists(word, lines):
            return False

        filtered_lines = [l for l in lines if _extract_word(l) != _extract_word(word)]

        with open(BAD_WORDS_FILE, 'w', encoding='utf-8') as f:
            f.writelines(filtered_lines)

        return True
    
    except Exception:
        return False