"""
clue.py — A single piece of evidence found in a room.

Python concepts: classes, instance attributes, mutable vs immutable,
magic methods (__repr__, __str__, __eq__, __hash__), @property, docstrings
"""

class Clue:
    """A piece of physical evidence found in a room of Blackwood Manor."""

    VALID_CATEGORIES = ["suspect", "weapon"]  # class attribute — shared by all instances

    def __init__(self, description, points_to, weight=0.5, category="suspect"):
        """
        Args:
            description: What the player reads when they find the clue.
            points_to:   Name of the suspect or weapon this implicates.
            weight:      Evidence strength from 0.0 (weak) to 1.0 (strong).
            category:    "suspect" or "weapon". Default is "suspect".
        """
        if not 0.0 <= weight <= 1.0:
            raise ValueError(f"Weight must be 0.0–1.0, got {weight}")

        self.__description = description   # immutable (private, name-mangled)
        self.__points_to   = points_to     # immutable (private, name-mangled)
        self.__weight      = weight        # immutable (private, name-mangled)
        self.category      = category      # public
        self.discovered    = False         # mutable — changes when player finds it

    # @property gives read-only access to private attributes
    @property
    def description(self): return self.__description

    @property
    def points_to(self): return self.__points_to

    @property
    def weight(self): return self.__weight

    def discover(self):
        """Mark this clue as found. Returns the description to show the player."""
        self.discovered = True
        return self.__description

    def summary(self):
        """Return a plain dict — used by Streamlit to display clue info."""
        return {
            "description": self.__description,
            "points_to":   self.__points_to,
            "weight":      self.__weight,
            "discovered":  self.discovered,
        }

    # Magic methods
    def __repr__(self):
        return f"Clue({self.__description!r} -> {self.__points_to})"

    def __str__(self):
        status = "[FOUND]" if self.discovered else "[?]"
        return f"{status} {self.__description}"

    def __eq__(self, other):
        if not isinstance(other, Clue): return NotImplemented
        return self.__description == other.__description

    def __hash__(self):
        return hash(self.__description)  # lets Clue be stored in a set


# All clues available in the game — clue_generator in utils.py picks from this list
ALL_CLUE_TEMPLATES = [
    Clue("A monogrammed handkerchief — initials P.P.",  "Professor Plum",    0.9),
    Clue("Reading glasses left open on the desk",       "Professor Plum",    0.7),
    Clue("A red lipstick mark on a wine glass",         "Miss Scarlet",      0.8),
    Clue("A scarlet hair ribbon on the door frame",     "Miss Scarlet",      0.7),
    Clue("A cigar stub with a gold band",               "Colonel Mustard",   0.8),
    Clue("Military boot prints in the dust",            "Colonel Mustard",   0.7),
    Clue("A peacock-blue feather on the floor",         "Mrs. Peacock",      0.7),
    Clue("A pearl earring from Mrs. Peacock's set",     "Mrs. Peacock",      0.9),
    Clue("A green tweed jacket button on the carpet",   "Mr. Green",         0.8),
    Clue("A white apron with a suspicious stain",       "Mrs. White",        0.8),
    Clue("Wax drippings in a trail across the floor",   "Candlestick",       0.7,  "weapon"),
    Clue("An empty bullet casing under the sofa",       "Revolver",          0.9,  "weapon"),
    Clue("Fibres from a thick rope on a hook",          "Rope",              0.8,  "weapon"),
    Clue("A bloodstain on the tablecloth",              "Knife",             0.8,  "weapon"),
    Clue("Rust marks on the Persian rug",               "Lead Pipe",         0.7,  "weapon"),
    Clue("Grease marks on the doorframe",               "Wrench",            0.6,  "weapon"),
]