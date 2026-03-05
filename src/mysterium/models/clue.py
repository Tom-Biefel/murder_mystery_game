"""
clue.py
-------
A Clue is a piece of physical evidence found in a room of Blackwood Manor.
Each clue has a description (what the player reads), a points_to field
(which suspect or weapon it implicates), and a weight (how strongly it points).

Python concepts covered in this file:
    - Classes and instances
    - Instance attributes (mutable and immutable)
    - Magic methods (__repr__, __str__, __eq__, __hash__)
    - Properties (@property) for read-only access
    - Hashable objects (Clue can be stored in sets and used as dict keys)
    - Docstrings
    - Type hints
    - Class attributes
    - Default arguments
"""


class Clue:
    """
    Represents a single piece of physical evidence found in a room.

    A Clue is immutable once created — its description, points_to, weight,
    and category cannot be changed after initialisation. Only the 'discovered'
    attribute changes (from False to True when the player finds the clue).

    Attributes:
        description (str): What the player reads when they find the clue.
                           e.g. "A torn page with Professor Plum's handwriting"
        points_to   (str): The name of the suspect or weapon this clue implicates.
                           e.g. "Professor Plum" or "Candlestick"
        weight    (float): How strongly this clue implicates points_to.
                           Range: 0.0 (weak hint) to 1.0 (definitive proof).
                           Default is 0.5 (moderate evidence).
        category    (str): What the clue points to — "suspect" or "weapon".
                           Default is "suspect".
        discovered (bool): Whether the player has already found this clue.
                           Starts as False, becomes True after room.search().

    Example:
        >>> clue = Clue("A torn glove near the fireplace", "Professor Plum", 0.8)
        >>> print(clue)
        [UNDISCOVERED] A torn glove near the fireplace → Professor Plum
        >>> clue.discovered = True
        >>> print(clue)
        [FOUND] A torn glove near the fireplace → Professor Plum
    """

    # ── Class attribute ───────────────────────────────────────────────────────
    # Shared across ALL Clue instances — not unique per clue
    # Used to validate the category when creating a clue
    VALID_CATEGORIES = ["suspect", "weapon", "room"]

    # ── Constructor ───────────────────────────────────────────────────────────

    def __init__(
        self,
        description: str,
        points_to: str,
        weight: float = 0.5,        # default argument — moderate evidence
        category: str = "suspect",  # default argument — most clues point to suspects
    ):
        """
        Initialise a new Clue.

        Args:
            description (str):   What the player reads when they find the clue.
            points_to   (str):   Suspect name or weapon name this clue implicates.
            weight      (float): Evidence strength from 0.0 to 1.0. Default 0.5.
            category    (str):   "suspect", "weapon", or "room". Default "suspect".

        Raises:
            ValueError: If weight is not between 0.0 and 1.0.
            ValueError: If category is not one of VALID_CATEGORIES.
        """
        # Validate inputs before storing
        if not 0.0 <= weight <= 1.0:
            raise ValueError(f"Weight must be between 0.0 and 1.0, got {weight}")

        if category not in self.VALID_CATEGORIES:
            raise ValueError(
                f"Category must be one of {self.VALID_CATEGORIES}, got '{category}'"
            )

        # Immutable attributes — stored with name-mangling (double underscore)
        # Name-mangling means Python renames __description to _Clue__description
        # This makes it very hard to accidentally overwrite from outside the class
        self.__description = description   # immutable
        self.__points_to   = points_to     # immutable
        self.__weight      = weight        # immutable
        self.__category    = category      # immutable

        # Mutable attribute — this one IS allowed to change during the game
        # It starts as False and becomes True when the player finds the clue
        self.discovered = False            # mutable

    # ── Properties (read-only access to private attributes) ──────────────────
    # @property turns a method into a readable attribute
    # e.g. clue.description works, but clue.description = "new" raises AttributeError

    @property
    def description(self) -> str:
        """The text the player reads when they find this clue."""
        return self.__description

    @property
    def points_to(self) -> str:
        """The suspect or weapon name this clue implicates."""
        return self.__points_to

    @property
    def weight(self) -> float:
        """How strongly this clue implicates points_to (0.0 to 1.0)."""
        return self.__weight

    @property
    def category(self) -> str:
        """Whether this clue points to a 'suspect', 'weapon', or 'room'."""
        return self.__category

    # ── Magic methods ─────────────────────────────────────────────────────────
    # Magic methods (dunder methods) define how Python's built-in operations
    # behave on our custom class

    def __repr__(self) -> str:
        """
        Developer-friendly string representation.
        Used when you print a Clue object in the Python console or in a list.

        Example:
            >>> clue = Clue("Torn glove", "Professor Plum", 0.8)
            >>> repr(clue)
            "Clue('Torn glove' -> Professor Plum, weight=0.8)"
        """
        return f"Clue({self.__description!r} -> {self.__points_to}, weight={self.__weight})"

    def __str__(self) -> str:
        """
        Player-friendly string representation.
        Used when the clue is displayed in the game UI.

        Example:
            >>> clue = Clue("Torn glove", "Professor Plum", 0.8)
            >>> str(clue)
            "[UNDISCOVERED] Torn glove → Professor Plum"
        """
        status = "[FOUND]" if self.discovered else "[UNDISCOVERED]"
        return f"{status} {self.__description} → {self.__points_to}"

    def __eq__(self, other: object) -> bool:
        """
        Two clues are equal if they have the same description.
        This lets us compare clues with == and use them in lists.

        Example:
            >>> c1 = Clue("Torn glove", "Professor Plum")
            >>> c2 = Clue("Torn glove", "Professor Plum")
            >>> c1 == c2
            True
        """
        if not isinstance(other, Clue):
            return NotImplemented
        return self.__description == other.__description

    def __hash__(self) -> int:
        """
        Makes Clue a hashable object — it can be stored in a set or used as a dict key.
        Python requires __hash__ when you define __eq__.

        This is used to prevent duplicate clues in a room:
            clue_set = {clue1, clue2, clue3}  # works because Clue is hashable

        Example:
            >>> c1 = Clue("Torn glove", "Professor Plum")
            >>> c2 = Clue("Torn glove", "Professor Plum")
            >>> len({c1, c2})   # set removes duplicate
            1
        """
        return hash(self.__description)

    def __lt__(self, other: "Clue") -> bool:
        """
        Allows sorting clues by weight (strongest evidence first).

        Example:
            >>> clues = [Clue("A", "Plum", 0.3), Clue("B", "Plum", 0.9)]
            >>> sorted(clues, reverse=True)  # strongest first
        """
        if not isinstance(other, Clue):
            return NotImplemented
        return self.__weight < other.__weight

    # ── Regular methods ───────────────────────────────────────────────────────

    def discover(self) -> str:
        """
        Mark this clue as discovered and return its description.
        Called when a player searches the room this clue is in.

        Returns:
            str: The clue description — shown to the player in the game.
        """
        self.discovered = True
        return self.__description

    def summary(self) -> dict:
        """
        Return a dictionary summary of this clue.
        Useful for saving game state to JSON and for the Streamlit UI.

        Returns:
            dict: All clue data as a plain dictionary.

        Example:
            >>> clue.summary()
            {
                'description': 'Torn glove near the fireplace',
                'points_to':   'Professor Plum',
                'weight':      0.8,
                'category':    'suspect',
                'discovered':  True
            }
        """
        return {
            "description": self.__description,
            "points_to":   self.__points_to,
            "weight":      self.__weight,
            "category":    self.__category,
            "discovered":  self.discovered,
        }


# ── Module-level clue templates ───────────────────────────────────────────────
# These are ALL the possible clues in the game.
# The clue_generator.py service will randomly pick from this list
# and distribute them across rooms at the start of each game.
#
# Format: Clue(description, points_to, weight, category)
# Higher weight = stronger evidence

ALL_CLUE_TEMPLATES = [

    # ── Clues pointing to Professor Plum ──────────────────────────────────────
    Clue("A monogrammed handkerchief with the initials P.P.",
         "Professor Plum", weight=0.8),
    Clue("Professor Plum's reading glasses left on the desk",
         "Professor Plum", weight=0.9),
    Clue("A torn page covered in academic handwriting",
         "Professor Plum", weight=0.7),
    Clue("An empty bottle of Plum's preferred ink",
         "Professor Plum", weight=0.6),

    # ── Clues pointing to Miss Scarlet ────────────────────────────────────────
    Clue("A red lipstick mark on a wine glass",
         "Miss Scarlet", weight=0.8),
    Clue("A scarlet hair ribbon caught on the door frame",
         "Miss Scarlet", weight=0.7),
    Clue("A torn piece of red fabric on a nail",
         "Miss Scarlet", weight=0.6),
    Clue("A calling card belonging to Miss Scarlet",
         "Miss Scarlet", weight=0.9),

    # ── Clues pointing to Colonel Mustard ────────────────────────────────────
    Clue("A cigar stub with a gold band — Mustard's brand",
         "Colonel Mustard", weight=0.8),
    Clue("Military boot prints in the dust",
         "Colonel Mustard", weight=0.7),
    Clue("A torn epaulette from a military uniform",
         "Colonel Mustard", weight=0.9),
    Clue("An empty whiskey flask monogrammed C.M.",
         "Colonel Mustard", weight=0.8),

    # ── Clues pointing to Mrs. Peacock ───────────────────────────────────────
    Clue("A peacock-blue feather on the floor",
         "Mrs. Peacock", weight=0.7),
    Clue("A pearl earring — part of Mrs. Peacock's set",
         "Mrs. Peacock", weight=0.9),
    Clue("A torn page from Mrs. Peacock's personal diary",
         "Mrs. Peacock", weight=0.8),
    Clue("Traces of expensive perfume near the window",
         "Mrs. Peacock", weight=0.6),

    # ── Clues pointing to Mr. Green ──────────────────────────────────────────
    Clue("A green tweed jacket button on the carpet",
         "Mr. Green", weight=0.8),
    Clue("A crumpled note in Mr. Green's handwriting",
         "Mr. Green", weight=0.9),
    Clue("Muddy footprints matching Mr. Green's shoe size",
         "Mr. Green", weight=0.7),
    Clue("A broken pen with Mr. Green's initials",
         "Mr. Green", weight=0.6),

    # ── Clues pointing to Mrs. White ─────────────────────────────────────────
    Clue("A white apron with a suspicious stain",
         "Mrs. White", weight=0.8),
    Clue("A kitchen knife missing from the set",
         "Mrs. White", weight=0.7),
    Clue("A note from Mrs. White arranging a secret meeting",
         "Mrs. White", weight=0.9),
    Clue("A white cotton thread caught on the cabinet door",
         "Mrs. White", weight=0.6),

    # ── Clues pointing to the Candlestick ────────────────────────────────────
    Clue("Wax drippings on the floor in a trail",
         "Candlestick", weight=0.7, category="weapon"),
    Clue("A scorch mark consistent with a heavy brass candlestick",
         "Candlestick", weight=0.8, category="weapon"),
    Clue("A dented candlestick holder with traces of hair",
         "Candlestick", weight=0.9, category="weapon"),

    # ── Clues pointing to the Knife ──────────────────────────────────────────
    Clue("A small bloodstain on the tablecloth",
         "Knife", weight=0.8, category="weapon"),
    Clue("A sharpening stone recently used",
         "Knife", weight=0.6, category="weapon"),
    Clue("A knife missing from the kitchen block",
         "Knife", weight=0.9, category="weapon"),

    # ── Clues pointing to the Lead Pipe ──────────────────────────────────────
    Clue("Rust marks on the Persian rug",
         "Lead Pipe", weight=0.7, category="weapon"),
    Clue("A heavy dent in the wall at head height",
         "Lead Pipe", weight=0.8, category="weapon"),
    Clue("Traces of lead paint on the floor",
         "Lead Pipe", weight=0.6, category="weapon"),

    # ── Clues pointing to the Revolver ───────────────────────────────────────
    Clue("An empty bullet casing under the sofa",
         "Revolver", weight=0.9, category="weapon"),
    Clue("The smell of gunpowder still in the air",
         "Revolver", weight=0.7, category="weapon"),
    Clue("A cleaning rod for a small calibre revolver",
         "Revolver", weight=0.6, category="weapon"),

    # ── Clues pointing to the Rope ───────────────────────────────────────────
    Clue("Fibres from a thick rope caught on a hook",
         "Rope", weight=0.8, category="weapon"),
    Clue("Burn marks on the banister consistent with rope friction",
         "Rope", weight=0.7, category="weapon"),
    Clue("A cut length of hemp rope behind the curtain",
         "Rope", weight=0.9, category="weapon"),

    # ── Clues pointing to the Wrench ─────────────────────────────────────────
    Clue("Grease marks on the doorframe",
         "Wrench", weight=0.6, category="weapon"),
    Clue("A wrench with traces of blood on the handle",
         "Wrench", weight=0.9, category="weapon"),
    Clue("Bolt marks on the floor where something was pried open",
         "Wrench", weight=0.7, category="weapon"),
]