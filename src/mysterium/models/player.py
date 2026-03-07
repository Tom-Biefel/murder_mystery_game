"""
player.py — The detective exploring Blackwood Manor.

Python concepts: classes, composition (Player HAS clues + evidence),
collections (deque), datetime + strftime, @property,
default arguments, mutable attributes, docstrings
"""

from collections import deque
from datetime import datetime


class Player:
    """The detective. Moves through rooms, collects clues, builds evidence."""

    def __init__(self, name, start_room="Hall"):
        """
        Args:
            name:       The player's name.
            start_room: Where the player begins. Default is "Hall".
        """
        self.name         = name
        self.current_room = start_room
        self.inventory    = []               # list of discovered Clue objects
        self.evidence     = {}              # {"Professor Plum": 1.6, "Scarlet": 0.8}
        self.move_history = deque(maxlen=10) # collections.deque — last 10 moves only

    def move(self, room_name):
        """Move player to room_name and log the move with a timestamp."""
        self.current_room = room_name
        timestamp = datetime.now().strftime("%H:%M:%S")  # datetime + strftime
        self.move_history.append((room_name, timestamp))

    def collect_clue(self, clue):
        """Add a clue to inventory and update the evidence dict."""
        self.inventory.append(clue)
        key = clue.points_to
        self.evidence[key] = self.evidence.get(key, 0) + clue.weight

    def evidence_summary(self):
        """Return evidence as percentage scores. Highest = most likely culprit."""
        total = sum(self.evidence.values()) or 1
        return {k: round((v / total) * 100, 1) for k, v in self.evidence.items()}

    @property
    def total_clues_found(self):
        """Read-only count of how many clues the player has found."""
        return len(self.inventory)

    def __repr__(self):
        return f"Player({self.name!r}, room={self.current_room!r})"

    def __str__(self):
        return f"Detective {self.name} — currently in the {self.current_room}"