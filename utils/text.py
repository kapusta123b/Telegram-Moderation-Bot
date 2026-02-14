from string import punctuation

from config.config import BAD_WORDS_FILE

with open(BAD_WORDS_FILE, encoding="utf-8") as f:
    BAD_WORDS = {line.strip().lower() for line in f if line.strip()}


def normalize(text: str) -> str:
    """
    Removes punctuation and converts text to lowercase for uniform comparison.
    """

    return text.translate(str.maketrans("", "", punctuation)).lower()


def contains_bad_word(text: str) -> bool:
    """
    Checks if the provided text contains any prohibited words from the blacklist.
    Supports both exact matches and substring detection.
    """

    normalized = normalize(text)
    words = normalized.split()

    if BAD_WORDS.intersection(words):
        return True

    for bad_word in BAD_WORDS:
        if bad_word in normalized:
            return True
    return False