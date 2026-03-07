"""
suspect.py — One of the six murder suspects.

Python concepts: classes, class attributes, instance attributes,
immutable attributes, magic methods, @property, default arguments, docstrings
"""

class Suspect:
    """One of the six characters who might be the murderer."""

    VALID_COLORS = ["red", "yellow", "blue", "purple", "green", "white"]  # class attribute

    def __init__(self, name, color, trait, home_room, alibi="No alibi provided."):
        """
        Args:
            name:      Full name of the suspect.
            color:     Their colour — must be in VALID_COLORS.
            trait:     Their personality (e.g. "cunning").
            home_room: The room where they live in the mansion.
            alibi:     Their alibi statement. Default = "No alibi provided."
        """
        if color not in self.VALID_COLORS:
            raise ValueError(f"Invalid color '{color}'. Must be one of {self.VALID_COLORS}")

        self.__name      = name       # immutable (private)
        self.__home_room = home_room  # immutable (private)
        self.color       = color      # public
        self.trait       = trait      # public
        self.alibi       = alibi      # public (default argument used above)
        self.eliminated  = False      # mutable — True when player rules them out

    @property
    def name(self): return self.__name

    @property
    def home_room(self): return self.__home_room

    def get_alibi(self):
        """Return the suspect's alibi with their name."""
        return f"{self.__name}: \"{self.alibi}\""

    def react(self):
        """Return an in-character reaction when accused."""
        reactions = {
            "Miss Scarlet":    "\"How daring of you, detective.\"",
            "Colonel Mustard": "\"Outrageous! I demand a solicitor!\"",
            "Mrs. Peacock":    "\"I beg your pardon?\"",
            "Professor Plum":  "\"Fascinating theory...\"",
            "Mr. Green":       "\"I — I had nothing to do with it!\"",
            "Mrs. White":      "\"Prove it.\"",
        }
        return f"{self.__name}: {reactions.get(self.__name, 'No comment.')}"

    # Magic methods
    def __repr__(self):
        return f"Suspect({self.__name!r}, room={self.__home_room!r})"

    def __str__(self):
        status = " [ELIMINATED]" if self.eliminated else ""
        return f"{self.__name} ({self.trait}){status}"

    def __eq__(self, other):
        if not isinstance(other, Suspect): return NotImplemented
        return self.__name == other.__name


# All 6 suspects — import this list wherever suspects are needed
ALL_SUSPECTS = [
    Suspect("Miss Scarlet",    "red",    "cunning",      "Lounge",
            "I was in the Lounge all evening."),
    Suspect("Colonel Mustard", "yellow", "aggressive",   "Billiard Room",
            "I was playing billiards alone."),
    Suspect("Mrs. Peacock",    "blue",   "deceptive",    "Conservatory",
            "I was tending to the orchids."),
    Suspect("Professor Plum",  "purple", "intelligent",  "Library",
            "I was reading. I never heard a thing."),
    Suspect("Mr. Green",       "green",  "nervous",      "Study",
            "I was writing letters in the study."),
    Suspect("Mrs. White",      "white",  "calm",         "Kitchen",
            "I was preparing supper. I never left."),
]