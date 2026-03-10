"""
suspect.py

Python concepts covered:
    - Classes and instances
    - Class attributes (VALID_COLORS)
    - Instance attributes (mutable: eliminated / immutable by convention: _name, _home_room)
    - Single underscore convention (Session 12)
    - Default arguments (alibi)
    - Magic methods: __repr__, __str__, __eq__
    - Docstrings
"""


class Suspect:
    """One of the six characters who might be the murderer."""

    valid_colors = ["red", "yellow", "blue", "purple", "green", "white"]

    def __init__(self, name, color, trait, home_room, alibi="No alibi provided."):
        """
        Args:
            name: Full name of the suspect.
            color: Their color.
            trait: Their personality (e.g. "cunning").
            home_room: The room where they live in the mansion.
            alibi: Their alibi statement. Default = "No alibi provided."
        """
        if color not in self.valid_colors:
            raise ValueError(f"Invalid color '{color}'. Must be one of {self.valid_colors}")

        self._name = name
        self._home_room = home_room

        self.color = color
        self.trait = trait
        self.alibi = alibi
        self.eliminated = False

    def name(self): 
        """Return the suspect's name."""
        return self._name

    def home_room(self): 
        """Return the room that the suspect lives in."""
        return self._home_room

    def get_alibi(self):
        """Return the suspect's alibi with their name."""
        return f"{self._name}: \"{self.alibi}\""

    def react(self):
        """Return an in-character reaction when accused."""
        reactions = {
            "Miss Scarlet": "\"How daring of you, detective.\"",
            "Colonel Mustard": "\"Outrageous! I demand a solicitor!\"",
            "Mrs. Peacock": "\"I beg your pardon?\"",
            "Professor Plum": "\"Fascinating theory...\"",
            "Mr. Green": "\"I — I had nothing to do with it!\"",
            "Mrs. White": "\"Prove it.\"",
        }
        return f"{self._name}: {reactions.get(self._name, 'No comment.')}"

    # Magic methods
    def __repr__(self):
        return f"Suspect({self._name!r}, room={self._home_room!r})"

    def __str__(self):
        status = " [ELIMINATED]" if self.eliminated else ""
        return f"{self._name} ({self.trait}){status}"

    def __eq__(self, other):
        if not isinstance(other, Suspect):
            return NotImplemented
        return self._name == other._name


# all 6 suspects
all_suspects = [
    Suspect("Miss Scarlet", "red", "cunning", "Lounge", "I was in the Lounge all evening."),
    Suspect("Colonel Mustard", "yellow", "aggressive", "Billiard Room", "I was playing billiards alone."),
    Suspect("Mrs. Peacock", "blue", "deceptive", "Conservatory", "I was tending to the orchids."),
    Suspect("Professor Plum", "purple", "intelligent", "Library", "I was reading. I never heard a thing."),
    Suspect("Mr. Green", "green", "nervous", "Study", "I was writing letters in the study."),
    Suspect("Mrs. White", "white", "calm", "Kitchen", "I was preparing supper. I never left."),
]
