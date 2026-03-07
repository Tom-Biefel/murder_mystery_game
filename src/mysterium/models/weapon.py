"""
weapon.py — One of the six possible murder weapons.

Python concepts: classes, class attributes, instance attributes,
immutable attributes, magic methods, @property, default arguments, docstrings
"""

class Weapon:
    """One of the six possible murder weapons in Blackwood Manor."""

    WEIGHT_OPTIONS = ["light", "medium", "heavy"]  # class attribute

    def __init__(self, name, weight_class="medium"):
        """
        Args:
            name:         The weapon's name. Immutable.
            weight_class: "light", "medium", or "heavy". Default is "medium".
        """
        if weight_class not in self.WEIGHT_OPTIONS:
            raise ValueError(f"weight_class must be one of {self.WEIGHT_OPTIONS}")

        self.__name      = name          # immutable (private)
        self.weight_class = weight_class # public

    @property
    def name(self): return self.__name

    def describe(self):
        """Return a readable sentence about this weapon."""
        return f"A {self.weight_class} {self.__name}."

    # Magic methods
    def __repr__(self):
        return f"Weapon({self.__name!r}, {self.weight_class})"

    def __str__(self):
        return self.__name

    def __eq__(self, other):
        if not isinstance(other, Weapon): return NotImplemented
        return self.__name == other.__name


# All 6 weapons — import this list wherever weapons are needed
ALL_WEAPONS = [
    Weapon("Candlestick", "light"),
    Weapon("Knife",       "light"),
    Weapon("Lead Pipe",   "heavy"),
    Weapon("Revolver",    "medium"),
    Weapon("Rope",        "medium"),
    Weapon("Wrench",      "heavy"),
]