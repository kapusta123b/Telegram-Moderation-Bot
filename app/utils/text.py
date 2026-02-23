from string import punctuation

import re

from config.config import BAD_WORDS_FILE

with open(BAD_WORDS_FILE, encoding="utf-8") as f:
    BAD_WORDS = {line.strip().lower() for line in f if line.strip()}

def normalize(text: str) -> str:
    """
    Removes punctuation and converts text to lowercase for uniform comparison.
    """

    return text.translate(str.maketrans("", "", punctuation)).lower()


def contains_bad_word(text: str) -> bool | list:
    """
    Checks if the provided text contains any prohibited words from the blacklist.
    Supports both exact matches and substring detection.
    """

    normalized = normalize(text)

    bad_words = []

    for bad_word in BAD_WORDS:
        if bad_word in normalized:
            bad_words.append(bad_word)
    
    if bad_words:
        return bad_words
        
    return False


def contains_link(text: str) -> bool:
    pattern = r'(https?://)?t\.me/[^\s]+'

    matches = re.findall(pattern, text)
    
    return bool(matches)