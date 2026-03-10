"""
room.py

Python concepts:
    - Classes and instances
    - Inheritance: SecretPassage extends Room
    - Composition: Room HAS Clue objects
    - *args: connect(*room_names)
    - Mutable instance attributes (neighbours, clues)
    - Magic methods: __repr__, __str__, __len__, __contains__
    - Default arguments (resident_suspect=None)
    - List comprehensions
    - Docstrings

"""

from mysterium.models.clue import Clue


class Room:
    """A location in the mansion. Can hold clues and connects to neighbours."""

    def __init__(self, name, description, resident_suspect=None):
        """
        Create a room.

        Args:
            name:The room's name.
            description: Informative text shown to the player.
            resident_suspect: Name of the suspect who lives here (or None).
        """

        self.name = name
        self.description = description
        self.resident_suspect = resident_suspect
        self.neighbours = []
        self.clues = []
        self.searched = False

    def connect(self, *room_names):
        """Connect this room to one or more neighbours. Uses *args."""
        for name in room_names:
            if name not in self.neighbours:
                self.neighbours.append(name)

    def add_clue(self, clue):
        """Add a Clue object to this room."""
        self.clues.append(clue)

    def search(self):
        """
        Search the room. Returns a list of all undiscovered clues and marks
        them as discovered. Uses a list comprehension.
        """
        found = [clue for clue in self.clues if not clue.discovered]
        for clue in found:
            clue.discover()
        self.searched = True
        return found

    def is_adjacent(self, room_name):
        """Return True if room_name shares a wall with this room."""
        return room_name in self.neighbours

    def get_resident_info(self):
        """Return a sentence about who lives here (or nobody)."""
        if self.resident_suspect:
            return f"{self.resident_suspect} resides in the {self.name}."
        return f"Nobody in particular lives in the {self.name}."

    # Magic methods
    def __repr__(self):
        return f"Room({self.name!r})"

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.clues)

    def __contains__(self, clue):
        return clue in self.clues


# Inheritance
class SecretPassage(Room):
    """
    A hidden room connected by a secret passage.
    Inherits everything from Room and adds passage-specific behaviour.

    - super().__init__() calls the parent Room constructor
    - adds a new attribute: leads_to
    - overrides get_resident_info() to mention the passage
    """

    def __init__(self, name, description, leads_to, resident_suspect=None):
        """
        Create a secret passage room.

        Args:
            name: The room's name.
            description: Description text.
            leads_to: Name of the room the passage connects to.
            resident_suspect: Optional suspect who hides here.
        """
        # Call the parent class constructor first
        super().__init__(name, description, resident_suspect)

        # Extra attribute only SecretPassage has
        self.leads_to = leads_to

    def get_resident_info(self):
        """Override parent method, also mentions the secret passage."""
        base_info = super().get_resident_info()  # reuse the parent's version
        return f"{base_info} A hidden passage leads to the {self.leads_to}."

    def __repr__(self):
        return f"SecretPassage({self.name!r} -> {self.leads_to!r})"
