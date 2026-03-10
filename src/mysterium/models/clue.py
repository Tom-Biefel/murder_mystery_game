"""
clue.py

Python concepts covered: 
    - classes and instances
    - class attributes
    - instance attributes (mutable & immutable)
    - magic methods
    - docstrings
"""


class Clue:
    """A piece of physical evidence found in a room of Blackwood Manor."""

    # class attribute shared by all instances
    valid_cats = ["suspect", "weapon"]

    def __init__(self, description, points_to, weight=0.5, category="suspect"):
        """
        Create a new clue.

        Args:
            description: What the player reads when they find the clue.
            points_to: Name of the suspect or weapon this implicates.
            weight: Evidence strength from 0.0 (weak) to 1.0 (strong). Default is 0.5.
            category: "suspect" or "weapon". Default is "suspect".
        """

        if not 0.0 <= weight <= 1.0:
            raise ValueError(f"Weight must be 0.0–1.0, got {weight}")
        if category not in self.valid_cats:
            raise ValueError(f"Category must be one of {self.valid_cats}")

        # immutable (private, name-mangled)
        self._description = description
        self._points_to = points_to
        self._weight = weight

        self.category = category
        self.discovered = False

    # Plain getter methods instead of @property (which wasn't covered in class)
    def get_description(self):
        """Return the clue's description text."""
        return self._description

    def get_points_to(self):
        """Return the name of the suspect or weapon this clue implicates."""
        return self._points_to

    def get_weight(self):
        """Return the evidence weight (0.0 – 1.0)."""
        return self._weight

    def discover(self):
        """Mark this clue as found. Returns the description to show the player."""
        self.discovered = True
        return self._description

    def summary(self):
        """Return a plain dictionary."""
        return {
            "description": self._description,
            "points_to": self._points_to,
            "weight": self._weight,
            "discovered": self.discovered,
        }

    # Magic methods
    def __repr__(self):
        return f"Clue({self._description!r} -> {self._points_to})"

    # Controls the way of displaying
    def __str__(self):
        status = "[FOUND]" if self.discovered else "[?]"
        return f"{status} {self._description}"

    def __eq__(self, other):
        if not isinstance(other, Clue): return NotImplemented
        return self._description == other._description

    def __hash__(self):
        return hash(self._description)


# All clues available in the game
all_clue_templates = [
    Clue("A monogrammed handkerchief with initials P.P.", "Professor Plum", 0.9),
    Clue("Reading glasses left open on the desk", "Professor Plum", 0.7),
    Clue("A red lipstick mark on a wine glass", "Miss Scarlet", 0.8),
    Clue("A scarlet hair ribbon on the door frame", "Miss Scarlet", 0.7),
    Clue("A cigar stub with a gold band", "Colonel Mustard", 0.8),
    Clue("Military boot prints in the dust", "Colonel Mustard", 0.7),
    Clue("A peacock-blue feather on the floor", "Mrs. Peacock", 0.7),
    Clue("A pearl earring from Mrs. Peacock's set", "Mrs. Peacock", 0.9),
    Clue("A green tweed jacket button on the carpet", "Mr. Green", 0.8),
    Clue("A white apron with a suspicious stain", "Mrs. White", 0.8),
    Clue("Wax drippings in a trail across the floor", "Candlestick", 0.7, "weapon"),
    Clue("An empty bullet casing under the sofa", "Revolver", 0.9, "weapon"),
    Clue("Fibres from a thick rope on a hook", "Rope", 0.8, "weapon"),
    Clue("A bloodstain on the tablecloth", "Knife", 0.8, "weapon"),
    Clue("Rust marks on the Persian rug", "Lead Pipe", 0.7, "weapon"),
    Clue("Grease marks on the doorframe", "Wrench", 0.6, "weapon"),
]
