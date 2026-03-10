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
    valid_cats = ["suspect", "weapon", "room"]

    def __init__(self, description, points_to, category="suspect"):
        """
        Create a new clue.

        Args:
            description: What the player reads when they find the clue.
            points_to: Name of the suspect or weapon this implicates.
            category: "suspect" or "weapon". Default is "suspect".
        """

        if category not in self.valid_cats:
            raise ValueError(f"Category must be one of {self.valid_cats}")

        # immutable (private, name-mangled)
        self._description = description
        self._points_to = points_to

        self.category = category
        self.discovered = False

    # Plain getter methods instead of @property (which wasn't covered in class)
    def get_description(self):
        """Return the clue's description text."""
        return self._description

    def get_points_to(self):
        """Return the name of the suspect or weapon this clue implicates."""
        return self._points_to

    def discover(self):
        """Mark this clue as found. Returns the description to show the player."""
        self.discovered = True
        return self._description

    def summary(self):
        """Return a plain dictionary."""
        return {
            "description": self._description,
            "points_to": self._points_to,
            "category": self.category,
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
    # Suspect clues: finding these CLEARLY EXONERATES that suspect
    Clue("Security footage confirms Professor Plum was elsewhere at the time of the crime.", "Professor Plum"),
    Clue("A verified lecture attendance sheet places Professor Plum away from the scene.", "Professor Plum"),
    Clue("Multiple witnesses confirm Miss Scarlet was seen in another wing.", "Miss Scarlet"),
    Clue("Miss Scarlet’s schedule was time-stamped and verified during the incident.", "Miss Scarlet"),
    Clue("Colonel Mustard’s boots were freshly polished and show no recent outdoor use.", "Colonel Mustard"),
    Clue("A signed officer’s log confirms Colonel Mustard never left his quarters.", "Colonel Mustard"),
    Clue("Mrs. Peacock was documented hosting guests at the time of the crime.", "Mrs. Peacock"),
    Clue("A written statement confirms Mrs. Peacock remained in plain sight all evening.", "Mrs. Peacock"),
    Clue("Mr. Green’s paperwork was timestamped, proving he was working elsewhere.", "Mr. Green"),
    Clue("Witness testimony confirms Mr. Green was occupied in another room.", "Mr. Green"),
    Clue("Mrs. White was accounted for in the kitchen under staff supervision.", "Mrs. White"),
    Clue("Kitchen staff confirm Mrs. White never left her post during the incident.", "Mrs. White"),

    # Weapon clues: finding these CLEARLY EXONERATES that weapon
    Clue("The candlestick was inspected and shows no signs of use.", "Candlestick", "weapon"),
    Clue("The revolver was found fully loaded and unfired.", "Revolver", "weapon"),
    Clue("The rope was coiled neatly and shows no tension or fibre damage.", "Rope", "weapon"),
    Clue("Forensics confirm the knife bears no blood or fingerprints.", "Knife", "weapon"),
    Clue("The lead pipe was clean and undisturbed in storage.", "Lead Pipe", "weapon"),
    Clue("The wrench was accounted for in the toolbox and unused.", "Wrench", "weapon"),

    # Room clues: finding these CLEARLY EXONERATES that room
    Clue("The kitchen shows no signs of struggle or disturbance.", "Kitchen", "room"),
    Clue("The ballroom floor was spotless and recently cleaned.", "Ballroom", "room"),
    Clue("The conservatory plants were undisturbed and intact.", "Conservatory", "room"),
    Clue("The billiard room was in perfect order with no damage.", "Billiard Room", "room"),
    Clue("The hall entrance mat shows no unusual markings.", "Hall", "room"),
    Clue("The library was quiet and untouched at the time of inspection.", "Library", "room"),
    Clue("The lounge furniture was undamaged and neatly arranged.", "Lounge", "room"),
    Clue("The dining room showed no evidence of conflict.", "Dining Room", "room"),
    Clue("The study desk remained orderly and undisturbed.", "Study", "room"),
    Clue("The wine cellar racks were intact with no signs of activity.", "Wine Cellar", "room"),
    Clue("The trophy room displayed no fallen items or disruption.", "Trophy Room", "room"),
]
