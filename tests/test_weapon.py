"""
test_weapon.py — Isolated unit tests for mysterium.models.weapon
"""

import pytest
from mysterium.models.weapon import Weapon, all_weapons


# Fixtures
@pytest.fixture
def weapon():
    return Weapon("Knife", "light")


# __init__
def test_weapon_name(weapon):
    assert weapon.name() == "Knife"


def test_weapon_weight_class(weapon):
    assert weapon.weight_class == "light"


def test_weapon_default_weight_class():
    w = Weapon("Rope")
    assert w.weight_class == "medium"


def test_invalid_weight_class_raises():
    with pytest.raises(ValueError):
        Weapon("Knife", "ultra-heavy")


# describe()
def test_describe_contains_name(weapon):
    assert "Knife" in weapon.describe()


def test_describe_contains_weight_class(weapon):
    assert "light" in weapon.describe()


# Magic methods
def test_str_returns_name(weapon):
    assert str(weapon) == "Knife"


def test_repr(weapon):
    assert "Knife" in repr(weapon)
    assert "light" in repr(weapon)


def test_eq_same_name():
    w1 = Weapon("Rope", "light")
    w2 = Weapon("Rope", "heavy")
    assert w1 == w2


def test_eq_different_name():
    w1 = Weapon("Rope", "medium")
    w2 = Weapon("Knife", "medium")
    assert w1 != w2


# all_weapons list
def test_all_weapons_has_six():
    assert len(all_weapons) == 6


def test_all_weapons_are_weapon_instances():
    assert all(isinstance(w, Weapon) for w in all_weapons)


def test_all_weapons_unique_names():
    names = [w.name() for w in all_weapons]
    assert len(names) == len(set(names))


def test_all_weapons_valid_weight_classes():
    for w in all_weapons:
        assert w.weight_class in Weapon.weight_options
