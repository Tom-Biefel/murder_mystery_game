"""
test_clue.py — Isolated unit tests for mysterium.models.clue

Tests each method of the Clue class independently.
"""

import pytest
from mysterium.models.clue import Clue, all_clue_templates as ALL_CLUE_TEMPLATES


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def basic_clue():
    return Clue("A red ribbon on the door", "Miss Scarlet", 0.8, "suspect")

@pytest.fixture
def weapon_clue():
    return Clue("Wax drippings across the floor", "Candlestick", 0.7, "weapon")


# ── __init__ ──────────────────────────────────────────────────────────────────

def test_clue_attributes_set_correctly(basic_clue):
    assert basic_clue.get_description() == "A red ribbon on the door"
    assert basic_clue.get_points_to() == "Miss Scarlet"
    assert basic_clue.get_weight() == 0.8
    assert basic_clue.category == "suspect"
    assert basic_clue.discovered is False

def test_clue_default_category():
    clue = Clue("Some evidence", "Professor Plum")
    assert clue.category == "suspect"
    assert clue.get_weight() == 0.5

def test_clue_invalid_weight_raises():
    with pytest.raises(ValueError):
        Clue("Bad clue", "Someone", weight=1.5)

def test_clue_invalid_category_raises():
    with pytest.raises(ValueError):
        Clue("Bad clue", "Someone", category="room")


# ── discover() ────────────────────────────────────────────────────────────────

def test_discover_marks_clue_as_found(basic_clue):
    assert basic_clue.discovered is False
    basic_clue.discover()
    assert basic_clue.discovered is True

def test_discover_returns_description(basic_clue):
    result = basic_clue.discover()
    assert result == "A red ribbon on the door"


# ── summary() ─────────────────────────────────────────────────────────────────

def test_summary_returns_dict(basic_clue):
    s = basic_clue.summary()
    assert s["description"] == "A red ribbon on the door"
    assert s["points_to"] == "Miss Scarlet"
    assert s["weight"] == 0.8
    assert s["discovered"] is False

def test_summary_discovered_updates(basic_clue):
    basic_clue.discover()
    assert basic_clue.summary()["discovered"] is True


# ── Magic methods ─────────────────────────────────────────────────────────────

def test_repr(basic_clue):
    assert "Miss Scarlet" in repr(basic_clue)

def test_str_undiscovered(basic_clue):
    assert "[?]" in str(basic_clue)

def test_str_discovered(basic_clue):
    basic_clue.discover()
    assert "[FOUND]" in str(basic_clue)

def test_eq_same_description():
    c1 = Clue("Same text", "Suspect A", 0.5)
    c2 = Clue("Same text", "Suspect B", 0.9)
    assert c1 == c2

def test_eq_different_description():
    c1 = Clue("Text A", "Suspect A", 0.5)
    c2 = Clue("Text B", "Suspect A", 0.5)
    assert c1 != c2

def test_hash_usable_in_set():
    c1 = Clue("Same text", "A", 0.5)
    c2 = Clue("Same text", "B", 0.9)
    s = {c1, c2}
    assert len(s) == 1


# ── ALL_CLUE_TEMPLATES ────────────────────────────────────────────────────────

def test_all_clue_templates_not_empty():
    assert len(ALL_CLUE_TEMPLATES) > 0

def test_all_clue_templates_are_clue_instances():
    assert all(isinstance(c, Clue) for c in ALL_CLUE_TEMPLATES)

def test_all_clue_templates_valid_categories():
    for clue in ALL_CLUE_TEMPLATES:
        assert clue.category in ("suspect", "weapon")
