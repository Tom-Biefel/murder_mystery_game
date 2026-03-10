"""
weapon.py

Python concepts covered:
    - Classes and instances
    - Class attributes (WEIGHT_OPTIONS)
    - Instance attributes (mutable and immutable by convention)
    - Single underscore convention (Session 12)
    - Default arguments
    - Magic methods: __repr__, __str__, __eq__
    - Docstrings
"""


class Weapon:
    """One of the six possible murder weapons in Blackwood Manor."""

    weight_options = ["light", "medium", "heavy"]  # class attribute

    def __init__(self, name, weight_class="medium"):
        """
        Creating a weapon.

        Args:
            name: The weapon's name. Immutable.
            weight_class: "light", "medium", or "heavy". Default is "medium".
        """
        if weight_class not in self.weight_options:
            raise ValueError(f"weight_class must be one of {self.weight_options}")

        self._name = name
        self.weight_class = weight_class

    def name(self): 
        "Return the weapon's name"
        return self._name

    def describe(self):
        """Return a readable sentence about this weapon."""
        return f"A {self.weight_class} {self._name}."

    # Magic methods
    def __repr__(self):
        return f"Weapon({self.__name!r}, {self.weight_class})"

    def __str__(self):
        return self.__name

    def __eq__(self, other):
        if not isinstance(other, Weapon): return NotImplemented
        return self.__name == other.__name


# all 6 weapons
all_weapons = [
    Weapon("Candlestick", "light"),
    Weapon("Knife", "light"),
    Weapon("Lead Pipe", "heavy"),
    Weapon("Revolver", "medium"),
    Weapon("Rope", "medium"),
    Weapon("Wrench", "heavy"),
]
