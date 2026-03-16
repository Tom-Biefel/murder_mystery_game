"""
player.py

Python concepts covered:
    - Classes and instances
    - Composition: Player HAS Clue objects (inventory) and move history
    - Collections: deque (from collections) for move history
    - Datetime + strftime for timestamping moves
    - Mutable instance attributes (inventory, evidence, move_history)
    - Default arguments (start_room)
    - Magic methods: __repr__, __str__
    - Docstrings
"""

from collections import deque
from datetime import datetime


class Player:
    """The detective. Moves through rooms, collects clues, builds evidence."""

    def __init__(self, name, start_room="Hall"):
        """
        Args:
            name: The player's name.
            start_room: Where the player begins. Default is "Hall".
        """
        self.name = name
        self.current_room = start_room

        # list of discovered Clue objects
        self.inventory = []

        # Notebook: sets of names the player has manually crossed out
        self.crossed_suspects = set()
        self.crossed_weapons = set()
        self.crossed_rooms = set()

        # Free-text notes
        self.notes = []

        # Movement log (max 10 entries)
        self.move_history = deque(maxlen=10)

    def move(self, room_name):
        """Move player to room_name and log the move with a timestamp."""
        self.current_room = room_name
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.move_history.append((room_name, timestamp))

    def collect_clue(self, clue):
        """Add a clue to inventory and update the evidence dict."""
        self.inventory.append(clue)

    def total_clues_found(self):
        """Read-only count of how many clues the player has found."""
        return len(self.inventory)

    def clues_summary(self):
        """
        Return a list of dicts describing every clue in inventory.
        """
        return [
            {
                "description": c.get_description(),
                "points_to": c.get_points_to(),
                "category": c.category,
            }
            for c in self.inventory
        ]

    def cross_out(self, category, name):
        """
        Mark a suspect, weapon, or room as eliminated in the notebook.

        Args:
            category: "suspect", "weapon", or "room".
            name: The name to cross out.
        """
        if category == "suspect":
            self.crossed_suspects.add(name)
        elif category == "weapon":
            self.crossed_weapons.add(name)
        elif category == "room":
            self.crossed_rooms.add(name)
        else:
            raise ValueError(f"Unknown category '{category}'. Use suspect/weapon/room.")

    def reinstate(self, category, name):
        """
        Remove a name from the crossed-out set (undo a cross-out).

        Args:
            category: "suspect", "weapon", or "room".
            name: The name to reinstate.
        """
        if category == "suspect":
            self.crossed_suspects.discard(name)
        elif category == "weapon":
            self.crossed_weapons.discard(name)
        elif category == "room":
            self.crossed_rooms.discard(name)
        else:
            raise ValueError(f"Unknown category '{category}'. Use suspect/weapon/room.")

    def notebook_state(self):
        """
        Return the full notebook as a dict of sets.
        """
        return {
            "crossed_suspects": self.crossed_suspects,
            "crossed_weapons": self.crossed_weapons,
            "crossed_rooms": self.crossed_rooms,
        }

    def add_note(self, text):
        """Let the player jot down a free-text note with a timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.notes.append(f"[{timestamp}] {text}")

    # magic methods
    def __repr__(self):
        return f"Player({self.name!r}, room={self.current_room!r})"

    def __str__(self):
        return f"Detective {self.name} currently in the {self.current_room}"
