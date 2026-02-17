from datetime import timedelta

from config.config import DEFAULT_MUTE_TIME


def get_mute_duration(mutes_count: int) -> timedelta:
    """
    Calculates the duration of a mute based on the user's violation history.
    """

    if mutes_count <= 5:
        return DEFAULT_MUTE_TIME.get(mutes_count, timedelta(hours=1))

    base_time = timedelta(days=1).total_seconds()
    extra_mutes = mutes_count - 5
    multiplier = 1.2**extra_mutes
    return timedelta(seconds=base_time * multiplier)