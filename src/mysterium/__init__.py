"""
mysterium – Digital version of the murder mystery game CLUE.

Public API:
    Game        – Main game engine. Instantiate to start a new game.
    CaseFile    – The sealed solution (suspect, weapon, room).
    build_mansion   – Build and wire the 11-room mansion dict.
    validate_name   – Validate a player name against the regex pattern.
"""

__version__ = "0.1.1"
__description__ = "Digital version of the murder mystery game CLUE."

from mysterium.game import Game, CaseFile, build_mansion, validate_name

__all__ = ["Game", "CaseFile", "build_mansion", "validate_name"]
