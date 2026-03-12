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
from mysterium.models.room import Room, SecretPassage, all_rooms
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
    Decorator: prints the function name and a timestamp every time it is called.
    Wraps a function and modifies its default behaviour (Session 10).
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
    Yields every clue from clue_list in a random order, one at a time.
    Uses yield instead of return, so values are produced lazily.
    The caller uses next() to pull out one clue at a time.

    Args:
        clue_list: The full list of available Clue objects.
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

    def solution(self):
        """Return the solution as a dict used by the accusation result screen."""
        return {
            "suspect": self._suspect,
            "weapon": self._weapon,
            "room": self._room,
        }


# Mansion builder
def build_mansion():
    """
    Build the mansion from all_rooms (defined in room.py) and wire up
    the connections between neighbours. Returns a dict of room_name -> Room.
    """

    fresh = {}
    for r in all_rooms:
        if isinstance(r, SecretPassage):
            fresh[r.name] = SecretPassage(r.name, r.description, r.leads_to, r.resident_suspect)
        else:
            fresh[r.name] = Room(r.name, r.description, r.resident_suspect)
    rooms = fresh

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
    # Secret rooms must also be reachable from their neighbours
    rooms["Kitchen"].connect("Wine Cellar")
    rooms["Study"].connect("Trophy Room")
    return rooms


# Game engine
class Game:
    """Main game engine that creates mansion, seals solution, drives gameplay."""

    def __init__(self, player_name, difficulty=None):
        """
        Start a new game.

        Args:
            player_name: The detective's name.
            difficulty: "easy", "medium", or "hard". Falls back to the DIFFICULTY value in .env, then "medium".
        """
        # validate the player name
        validate_name(player_name)

        # os.getenv reads the .env file (loaded above with load_dotenv)
        self.difficulty = difficulty or os.getenv("DIFFICULTY", "medium")
        self.rooms = build_mansion()
        self.player = Player(player_name)
        self.game_over = False

        self.case = CaseFile(
            suspect = random.choice(all_suspects).name(),
            weapon = random.choice(all_weapons).name(),
            room = random.choice(list(self.rooms.keys())),
        )

        self._seed_clues()

    def _seed_clues(self):
        """
        Distribute clues evenly across all rooms using the clue_generator.
        """
        solution = self.case.solution()

        clues_per_room = {"easy": 3, "medium": 2, "hard": 1}
        n = clues_per_room.get(self.difficulty, 2)

        # Only keep clues that do NOT point at the actual answer
        suspect_clues = [
            c for c in all_clue_templates
            if c.category == "suspect"
            and c.get_points_to() != solution["suspect"]
        ]
        weapon_clues = [
            c for c in all_clue_templates
            if c.category == "weapon"
            and c.get_points_to() != solution["weapon"]
        ]

        room_clues = [
            c for c in all_clue_templates
            if c.category == "room"
            and c.get_points_to() != solution["room"]
        ]

        # must-place, so every innocent suspect, weapon, and room appears at least once.
        seen = set()
        must_place = []
        for pool in (suspect_clues, weapon_clues, room_clues):
            by_entity = {}
            for c in pool:
                entity = c.get_points_to()
                if entity not in by_entity:
                    by_entity[entity] = c
            for c in by_entity.values():
                must_place.append(c)
                seen.add(c)

        # Shuffle must-place clues and assign one to each room first
        random.shuffle(must_place)
        rooms_list = list(self.rooms.values())

        for clue in must_place:
            # only choose rooms that still have space (< n clues)
            available_rooms = [r for r in rooms_list if len(r.clues) < n]

            if not available_rooms:
                break  # all rooms are full for this difficulty

            random.choice(available_rooms).add_clue(clue)

        # fill remaining slots with alternating suspect/weapon clues
        extra_pools = [
            clue_generator([c for c in suspect_clues if c not in seen], len(suspect_clues)),
            clue_generator([c for c in weapon_clues if c not in seen], len(weapon_clues)),
            clue_generator([c for c in room_clues if c not in seen], len(room_clues)),
        ]
        for room in rooms_list:
            slots = n - len(room.clues)
            for i in range(slots):
                gen = extra_pools[i % 3]
                try:
                    room.add_clue(next(gen))
                except StopIteration:
                    pass

    @log_action   # decorator defined above: logs every move with a timestamp
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

    def cross_out(self, category, name):
        """
        Cross out a suspect, weapon, or room in the player's notebook.

        Args:
            category: "suspect", "weapon", or "room".
            name: The exact name to cross out.
        """
        self.player.cross_out(category, name)

    def reinstate(self, category, name):
        """
        Undo a cross-out in the player's notebook.

        Args:
            category: "suspect", "weapon", or "room".
            name: The exact name to reinstate.
        """
        self.player.reinstate(category, name)

    def accuse(self, suspect, weapon, room):
        """
        Make a final accusation. Always sets game_over = True and always
        reveals the correct solution regardless of whether the guess was right.

        Returns:
            A dict with keys: "correct" (bool), "message" (str), "solution" (dict).
        """
        self.game_over = True
        correct = self.case.check(suspect, weapon, room)
        return {
            "correct": correct,
            "message": ("Correct! " if correct else "Wrong! ") + self.case.reveal(),
            "solution": self.case.solution(),
        }

    def status(self):
        """Return current game state as a dict."""
        return {
            "player": self.player.name,
            "room": self.player.current_room,
            "clues_found": self.player.total_clues_found(),
            "move_history": list(self.player.move_history),
            "game_over": self.game_over,
        }
