__version__ = "0.1.1"
__description__ = "Digital version of the murder mystery game CLUE."

from mysterium.game import Game, CaseFile, build_mansion, validate_name

__all__ = ["Game", "CaseFile", "build_mansion", "validate_name"]
