"""
player.py

Python concepts covered:
    - Classes and instances
    - Composition: Player HAS Clue objects (inventory) and move history
    - Collections: deque (from collections) for move history
    - Datetime + strftime for timestamping moves
    - Mutable instance attributes (inventory, evidence, move_history)
    - Default arguments (start_room)
    - **kwargs: update_profile() accepts extra keyword options
    - Magic methods: __repr__, __str__
    - Docstrings
"""

from collections import deque
from datetime import datetime
from mysterium.models.clue import get_weight()



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
        self.evidence = {}
        self.move_history = deque(maxlen=10)
        self.notes = []

    def move(self, room_name):
        """Move player to room_name and log the move with a timestamp."""
        self.current_room = room_name
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.move_history.append((room_name, timestamp))

    def collect_clue(self, clue):
        """Add a clue to inventory and update the evidence dict."""
        self.inventory.append(clue)
        key = clue.get_points_to()
        self.evidence[key] = self.evidence.get(key, 0) + clue.get_weight()

    def add_note(self, text):
        "Let the player note down free-text notes"
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.notes.append(f"[{timestamp}] {text}")

    def evidence_summary(self):
        """Return evidence as percentage scores. Highest = most likely culprit."""
        total = sum(self.evidence.values()) or 1
        return {k: round((v / total) * 100, 1) for k, v in self.evidence.items()}

    def total_clues_found(self):
        """Read-only count of how many clues the player has found."""
        return len(self.inventory)

    # magic methods
    def __repr__(self):
        return f"Player({self.name!r}, room={self.current_room!r})"

    def __str__(self):
        return f"Detective {self.name} currently in the {self.current_room}"
