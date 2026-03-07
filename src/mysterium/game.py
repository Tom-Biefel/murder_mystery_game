"""
game.py — The game engine. Ties every other class together.

Python concepts: classes, composition, .env (dotenv), decorators applied,
random, list comprehensions, mutable attributes, docstrings
"""

import os
import random
from dotenv import load_dotenv

from mysterium.models.clue    import ALL_CLUE_TEMPLATES
from mysterium.models.room    import Room
from mysterium.models.player  import Player
from mysterium.models.suspect import ALL_SUSPECTS
from mysterium.models.weapon  import ALL_WEAPONS
from mysterium.utils          import log_action, clue_generator

load_dotenv()  # reads the .env file — e.g. DIFFICULTY=hard


# ── CaseFile — the sealed solution ────────────────────────────────────────────

class CaseFile:
    """Holds the sealed solution: one suspect, one weapon, one room."""

    def __init__(self, suspect, weapon, room):
        self.suspect = suspect  # the real murderer's name
        self.weapon  = weapon   # the real weapon's name
        self.room    = room     # the real room's name

    def check(self, suspect, weapon, room):
        """Return True if the accusation matches the sealed solution."""
        return self.suspect == suspect and self.weapon == weapon and self.room == room

    def reveal(self):
        """Return the full solution as a string."""
        return f"It was {self.suspect} with the {self.weapon} in the {self.room}!"


# ── Mansion builder ───────────────────────────────────────────────────────────

def build_mansion():
    """Create all 9 rooms, connect them as a 3x3 grid, return a dict."""
    rooms = {
        "Kitchen":      Room("Kitchen",      "A cold stone kitchen.",          "Mrs. White"),
        "Ballroom":     Room("Ballroom",      "A grand ballroom, empty now."),
        "Conservatory": Room("Conservatory",  "Glass walls, orchids everywhere.", "Mrs. Peacock"),
        "Billiard Room":Room("Billiard Room", "A green baize table, untouched.", "Colonel Mustard"),
        "Hall":         Room("Hall",          "The entrance hall. Portraits watch you."),
        "Library":      Room("Library",       "Shelves of dusty books.",         "Professor Plum"),
        "Lounge":       Room("Lounge",        "Velvet chairs, a cold fireplace.", "Miss Scarlet"),
        "Dining Room":  Room("Dining Room",   "A long mahogany table."),
        "Study":        Room("Study",         "Papers scattered everywhere.",    "Mr. Green"),
    }
    # Connect rooms as a 3x3 grid (share a wall = adjacent)
    rooms["Kitchen"].connect("Ballroom", "Billiard Room", "Hall")
    rooms["Ballroom"].connect("Kitchen", "Conservatory", "Hall")
    rooms["Conservatory"].connect("Ballroom", "Library", "Hall")
    rooms["Billiard Room"].connect("Kitchen", "Hall", "Lounge")
    rooms["Hall"].connect("Kitchen", "Ballroom", "Conservatory",
                          "Billiard Room", "Library", "Lounge", "Dining Room", "Study")
    rooms["Library"].connect("Conservatory", "Hall", "Study")
    rooms["Lounge"].connect("Billiard Room", "Hall", "Dining Room")
    rooms["Dining Room"].connect("Hall", "Lounge", "Study")
    rooms["Study"].connect("Library", "Hall", "Dining Room")
    return rooms


# ── Game engine ────────────────────────────────────────────────────────────────

class Game:
    """Main game engine — creates mansion, seals solution, drives gameplay."""

    def __init__(self, player_name, difficulty=None):
        self.difficulty = difficulty or os.getenv("DIFFICULTY", "medium")  # reads .env
        self.rooms      = build_mansion()
        self.player     = Player(player_name)
        self.case       = CaseFile(
            suspect = random.choice(ALL_SUSPECTS).name,
            weapon  = random.choice(ALL_WEAPONS).name,
            room    = random.choice(list(self.rooms.keys())),
        )
        self.game_over  = False
        self._seed_clues()

    def _seed_clues(self):
        """Distribute clues into rooms using the clue_generator."""
        gen = clue_generator(ALL_CLUE_TEMPLATES, len(ALL_CLUE_TEMPLATES))
        for i, room in enumerate(self.rooms.values()):
            for _ in range(2):                 # 2 clues per room
                try:
                    room.add_clue(next(gen))
                except StopIteration:
                    break

    @log_action  # decorator from utils.py — logs every move with timestamp
    def move(self, room_name):
        """Move the player to room_name if it is adjacent. Returns True/False."""
        current = self.rooms[self.player.current_room]
        if not current.is_adjacent(room_name):
            print(f"Cannot move to {room_name} — not adjacent.")
            return False
        self.player.move(room_name)
        return True

    def search(self):
        """Search the current room. Returns list of found clues."""
        room  = self.rooms[self.player.current_room]
        found = room.search()
        for clue in found:
            self.player.collect_clue(clue)
        return found

    def accuse(self, suspect, weapon, room):
        """Make a final accusation. Sets game_over = True."""
        self.game_over = True
        if self.case.check(suspect, weapon, room):
            return {"correct": True,  "message": "CORRECT! " + self.case.reveal()}
        return {"correct": False, "message": f"Wrong! The real answer: {self.case.reveal()}"}

    def status(self):
        """Return current game state as a dict — used by Streamlit."""
        return {
            "player":      self.player.name,
            "room":        self.player.current_room,
            "clues_found": self.player.total_clues_found,
            "evidence":    self.player.evidence_summary(),
            "game_over":   self.game_over,
        }