"""
mysterium.models – Data models for Blackwood Manor.

Classes:
    Clue            – A piece of physical evidence found in a room.
    Player          – The detective who moves through rooms and collects clues.
    Room            – A location in the mansion.
    SecretPassage   – A hidden room connected by a secret passage (extends Room).
    Suspect         – One of the six characters who might be the murderer.
    Weapon          – One of the six possible murder weapons.

Data:
    all_clue_templates  – All clue objects available in the game.
    all_rooms           – All 11 rooms of Blackwood Manor.
    all_suspects        – All 6 suspects.
    all_weapons         – All 6 weapons.
"""

from mysterium.models.clue import Clue, all_clue_templates
from mysterium.models.player import Player
from mysterium.models.room import Room, SecretPassage, all_rooms
from mysterium.models.suspect import Suspect, all_suspects
from mysterium.models.weapon import Weapon, all_weapons

__all__ = [
    "Clue", "all_clue_templates",
    "Player",
    "Room", "SecretPassage", "all_rooms",
    "Suspect", "all_suspects",
    "Weapon", "all_weapons",
]
