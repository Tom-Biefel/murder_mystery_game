"""
test_suspect.py — Isolated unit tests for mysterium.models.suspect
"""

import pytest
from mysterium.models.suspect import Suspect, all_suspects


# Fixtures
@pytest.fixture
def suspect():
    return Suspect("Miss Scarlet", "red", "cunning", "Lounge", "I was in the Lounge all evening.")


# __init__
def test_suspect_name(suspect):
    assert suspect.name() == "Miss Scarlet"


def test_suspect_home_room(suspect):
    assert suspect.home_room() == "Lounge"


def test_suspect_color(suspect):
    assert suspect.color == "red"


def test_suspect_not_eliminated_by_default(suspect):
    assert suspect.eliminated is False


def test_suspect_default_alibi():
    s = Suspect("Mr. Green", "green", "nervous", "Study")
    assert s.alibi == "No alibi provided."


def test_invalid_color_raises():
    with pytest.raises(ValueError):
        Suspect("Unknown", "pink", "odd", "Hall")


# react()
def test_react_returns_string(suspect):
    assert isinstance(suspect.react(), str)


def test_react_contains_name(suspect):
    assert "Miss Scarlet" in suspect.react()


def test_react_unknown_suspect():
    s = Suspect("Unknown Person", "green", "shy", "Hall")
    assert "No comment." in s.react()


def test_get_alibi_contains_name_and_text(suspect):
    alibi = suspect.get_alibi()
    assert "Miss Scarlet" in alibi
    assert "Lounge" in alibi


# Magic methods
def test_str_not_eliminated(suspect):
    assert "[ELIMINATED]" not in str(suspect)


def test_str_eliminated(suspect):
    suspect.eliminated = True
    assert "[ELIMINATED]" in str(suspect)


def test_repr(suspect):
    assert "Miss Scarlet" in repr(suspect)
    assert "Lounge" in repr(suspect)


def test_eq_same_name():
    s1 = Suspect("Professor Plum", "purple", "smart", "Library")
    s2 = Suspect("Professor Plum", "purple", "clever", "Study")
    assert s1 == s2


def test_eq_different_name():
    s1 = Suspect("Miss Scarlet", "red", "cunning", "Lounge")
    s2 = Suspect("Mr. Green", "green", "nervous", "Study")
    assert s1 != s2


def test_eq_non_suspect_returns_notimplemented(suspect):
    assert suspect.__eq__("not a suspect") is NotImplemented


# all_suspects list
def test_all_suspects_has_six():
    assert len(all_suspects) == 6


def test_all_suspects_are_suspect_instances():
    assert all(isinstance(s, Suspect) for s in all_suspects)


def test_all_suspects_unique_names():
    names = [s.name() for s in all_suspects]
    assert len(names) == len(set(names))


def test_all_suspects_valid_colors():
    for s in all_suspects:
        assert s.color in Suspect.valid_colors
