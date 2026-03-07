"""
room.py — A location in Blackwood Manor.

Python concepts: classes, composition (Room HAS Clues), *args,
magic methods (__repr__, __str__, __len__, __contains__),
list comprehensions, mutable attributes, docstrings
"""

from mysterium.models.clue import Clue


class Room:
    """A location in the mansion. Can hold clues and connects to neighbours."""

    def __init__(self, name, description, resident_suspect=None):
        """
        Args:
            name:             The room's name.
            description:      Flavour text shown to the player.
            resident_suspect: Name of the suspect who lives here (or None).
        """
        self.name             = name
        self.description      = description
        self.resident_suspect = resident_suspect  # default argument = None
        self.neighbours       = []               # mutable — filled by connect()
        self.clues            = []               # mutable — composition with Clue
        self.searched         = False            # mutable — True after player searches

    def connect(self, *room_names):
        """Connect this room to one or more neighbours. Uses *args."""
        for name in room_names:
            if name not in self.neighbours:
                self.neighbours.append(name)

    def add_clue(self, clue):
        """Add a Clue object to this room."""
        self.clues.append(clue)

    def search(self):
        """Return all undiscovered clues and mark them as discovered."""
        found = [c for c in self.clues if not c.discovered]  # list comprehension
        for clue in found:
            clue.discover()
        self.searched = True
        return found

    def is_adjacent(self, room_name):
        """Return True if room_name shares a wall with this room."""
        return room_name in self.neighbours

    # Magic methods
    def __repr__(self):
        return f"Room({self.name!r})"

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.clues)          # len(room) = number of clues in it

    def __contains__(self, clue):
        return clue in self.clues       # 'clue in room' works because of this