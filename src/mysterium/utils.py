"""
utils.py — Reusable utilities: decorator, generator, regex validator.

Python concepts: decorators, functools.wraps, generators (yield),
regular expressions (re.compile), functions, docstrings

No dependencies on other mysterium files — build this first!
"""

import re
import random
from functools import wraps
from datetime import datetime


# ── 1. DECORATOR ──────────────────────────────────────────────────────────────

def log_action(func):
    """
    Decorator — prints the function name and timestamp every time it is called.
    Apply with @log_action above any method in game.py.
    """
    @wraps(func)   # preserves the original function's __name__ and __doc__
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {func.__name__} called")
        result = func(*args, **kwargs)
        print(f"[{timestamp}] {func.__name__} done")
        return result
    return wrapper


# ── 2. GENERATOR ──────────────────────────────────────────────────────────────

def clue_generator(clue_list, n):
    """
    Generator — yields n randomly chosen clues from clue_list, one at a time.
    Uses yield instead of return, so values are produced lazily.

    Usage:
        gen = clue_generator(ALL_CLUE_TEMPLATES, 3)
        print(next(gen))   # first clue
        print(next(gen))   # second clue
    """
    pool = random.sample(clue_list, min(n, len(clue_list)))
    for clue in pool:
        yield clue   # yield — this is what makes it a generator


# ── 3. REGEX VALIDATOR ────────────────────────────────────────────────────────

NAME_PATTERN = re.compile(r"^[A-Za-z ]{2,20}$")  # compiled once at module level

def validate_name(name):
    """
    Validate a player name using a regular expression.
    Allows letters and spaces only, 2–20 characters.

    Raises:
        ValueError: if the name does not match the pattern.
    """
    if not NAME_PATTERN.match(name.strip()):
        raise ValueError(
            f"Invalid name {name!r}. Use letters only, 2–20 characters."
        )
    return True