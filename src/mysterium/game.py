"""
game.py (equivalent to main.py)

Python concepts covered:
    - Classes and instances (Game, CaseFile)
    - Composition: Game HAS Player, Rooms, CaseFile
    - .env with python-dotenv (os.getenv)
    - Decorators: @log_action applied to move()
    - Generators: clue_generator() used in _seed_clues()
    - List comprehensions
    - For loops and while loops
    - Mutable instance attributes
    - Docstrings
"""

import os
import re
import random
from datetime import datetime
from dotenv import load_dotenv

from mysterium.models.clue import all_clue_templates
from mysterium.models.room import Room, SecretPassage
from mysterium.models.player import Player
from mysterium.models.suspect import all_suspects
from mysterium.models.weapon import all_weapons

load_dotenv()

# Global scope
name_pattern = re.compile(r"^[A-Za-z ]{2,20}$")
env_file_path = os.path.join(os.path.dirname(__file__), ".env")


# decorator
def log_action(func):
    """
    Decorator — prints the function name and a timestamp every time it is called.
    Wraps a function and modifies its default behaviour (Session 10).

    Usage: place @log_action above any method to activate it.
    """
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {func.__name__} called")
        result = func(*args, **kwargs)
        return result
    return wrapper


# generator
def clue_generator(clue_list, n):
    """
    Yields up to n randomly chosen clues from clue_list, one at a time.
    Uses yield instead of return, so values are produced lazily.
    The caller uses next() to pull out one clue at a time.

    Args:
        clue_list: The full list of available Clue objects.
        n: How many clues to yield in total.
    """
    pool = random.sample(clue_list, min(n, len(clue_list)))
    for clue in pool:
        yield clue


# regex validator
def validate_name(name):
    """
    Validate a player name using a regular expression.
    Allows letters and spaces only, between 2 and 20 characters.
    Uses the global name_pattern compiled at the top of this file.

    Raises:
        ValueError if the name does not match the pattern.
    """
    if not name_pattern.match(name.strip()):
        raise ValueError(
            f"Invalid name {name!r}. Use letters and spaces only, 2–20 characters."
        )
    return True


# CaseFile: the sealed solution
class CaseFile:
    """Holds the sealed solution: one suspect, one weapon, one room."""

    def __init__(self, suspect, weapon, room):
        """
        Holds the sealed solution: one suspect name, one weapon name, one room name.
        Nobody (not even the player) should be able to read these until the accusation.
        """
        self._suspect = suspect
        self._weapon = weapon
        self._room = room

    def check(self, suspect, weapon, room):
        """Return True if the accusation matches the sealed solution."""
        return (
            self._suspect == suspect and
            self._weapon == weapon and
            self._room == room
        )

    def reveal(self):
        """Return the full solution as a string."""
        return f"It was {self._suspect} with the {self._weapon} in the {self._room}!"


# Mansion builder
def build_mansion():
    """Create all 9 rooms, connect them as a 3x3 grid, return a dict."""
    rooms = {
        "Kitchen": Room("Kitchen", "A cold stone kitchen.", "Mrs. White"),
        "Ballroom": Room("Ballroom", "A grand ballroom, empty now."),
        "Conservatory": Room("Conservatory", "Glass walls, orchids everywhere.", "Mrs. Peacock"),
        "Billiard Room": Room("Billiard Room", "A green baize table, untouched.", "Colonel Mustard"),
        "Hall": Room("Hall", "The entrance hall. Portraits watch you."),
        "Library": Room("Library", "Shelves of dusty books.", "Professor Plum"),
        "Lounge": Room("Lounge",  "Velvet chairs, a cold fireplace.", "Miss Scarlet"),
        "Dining Room": Room("Dining Room", "A long mahogany table."),
        "Study": Room("Study", "Papers scattered everywhere.", "Mr. Green"),
        # secret passages
        "Wine Cellar": SecretPassage("Wine Cellar", "Damp stone walls and dusty bottles.", leads_to="Kitchen"),
        "Trophy Room": SecretPassage("Trophy Room", "Hunting trophies and faded portraits.", leads_to="Study"),
    }
    # Connect rooms as a 3x3 grid (share a wall = adjacent)
    rooms["Kitchen"].connect("Ballroom", "Billiard Room", "Hall")
    rooms["Ballroom"].connect("Kitchen", "Conservatory", "Hall")
    rooms["Conservatory"].connect("Ballroom", "Library", "Hall")
    rooms["Billiard Room"].connect("Kitchen", "Hall", "Lounge")
    rooms["Hall"].connect("Kitchen", "Ballroom", "Conservatory", "Billiard Room", "Library", "Lounge", "Dining Room", "Study")
    rooms["Library"].connect("Conservatory", "Hall", "Study")
    rooms["Lounge"].connect("Billiard Room", "Hall", "Dining Room")
    rooms["Dining Room"].connect("Hall", "Lounge", "Study")
    rooms["Study"].connect("Library", "Hall", "Dining Room")
    rooms["Wine Cellar"].connect("Kitchen")
    rooms["Trophy Room"].connect("Study")
    return rooms


# Game engine
class Game:
    """Main game engine that creates mansion, seals solution, drives gameplay."""

    def __init__(self, player_name, difficulty=None):
        """
        Start a new game.

        Args:
            player_name : The detective's name.
            difficulty  : "easy", "medium", or "hard". Falls back to the DIFFICULTY value in .env, then "medium".
        """
        # validate the player name
        validate_name(player_name)

        # os.getenv reads the .env file (loaded above with load_dotenv)
        self.difficulty = difficulty or os.getenv("DIFFICULTY", "medium")
        self.rooms = build_mansion()
        self.player = Player(player_name)
        self.case = CaseFile(
            suspect = random.choice(all_suspects).name,
            weapon = random.choice(all_weapons).name,
            room = random.choice(list(self.rooms.keys())),
        )
        self.game_over = False
        self._seed_clues()

    def _seed_clues(self):
        """
        Distribute clues into rooms using the clue_generator.
        More clues on easy, fewer on hard.
        """
        clues_per_room = {"easy": 3, "medium": 2, "hard": 1}
        n = clues_per_room.get(self.difficulty, 2)

        # clue_generator yields one clue at a time — we pull with next()
        gen = clue_generator(all_clue_templates, len(all_clue_templates))
        for room in self.rooms.values():
            for _ in range(n):
                try:
                    room.add_clue(next(gen))
                except StopIteration:
                    break   # generator exhausted — stop distributing

    @log_action   # decorator defined above — logs every move with a timestamp
    def move(self, room_name):
        """
        Move the player to room_name if it is adjacent to the current room.
        Returns True on success, False if the move is not allowed.
        """
        current = self.rooms[self.player.current_room]
        if not current.is_adjacent(room_name):
            return False
        self.player.move(room_name)
        room = self.rooms[room_name]
        # If it is a SecretPassage, hint at the hidden exit
        if isinstance(room, SecretPassage):
            print(f"  [A hidden passage here leads to the {room.leads_to}...]")
        return True
    
    def use_passage(self):
        """
        If the player is in a SecretPassage room, teleport them through it.
        Returns the destination room name, or None if there is no passage here.
        """
        current_room = self.rooms[self.player.current_room]
        if isinstance(current_room, SecretPassage):
            destination = current_room.leads_to
            self.player.move(destination)
            return destination
        return None

    def search(self):
        """
        Search the current room for clues.
        Returns a list of clue description strings found.
        """
        room = self.rooms[self.player.current_room]
        found = room.search()
        for clue in found:
            self.player.collect_clue(clue)

        return [clue.get_description() for clue in found]

    def accuse(self, suspect, weapon, room):
        """Make a final accusation. Sets game_over = True."""
        self.game_over = True
        if self.case.check(suspect, weapon, room):
            return {"correct": True, "message": "Correct! " + self.case.reveal()}
        return {"correct": False, "message": f"Wrong! The real answer: {self.case.reveal()}"}

    def status(self):
        """Return current game state as a dict — used by Streamlit."""
        return {
            "player": self.player.name,
            "room": self.player.current_room,
            "clues_found": self.player.total_clues_found(),
            "evidence": self.player.evidence_summary(),
            "move_history": list(self.player.move_history),
            "game_over": self.game_over,
        }
