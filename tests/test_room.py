"""
test_room.py — Isolated unit tests for mysterium.models.room
"""

import pytest
from mysterium.models.room import Room, SecretPassage
from mysterium.models.clue import Clue


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def room():
    return Room("Library", "Dusty books everywhere.", "Professor Plum")

@pytest.fixture
def empty_room():
    return Room("Hall", "A large entrance hall.")

@pytest.fixture
def clue():
    return Clue("Reading glasses on the desk", "Professor Plum", 0.7)

@pytest.fixture
def passage():
    return SecretPassage("Wine Cellar", "Damp stone walls.", leads_to="Kitchen")


# ── __init__ ──────────────────────────────────────────────────────────────────

def test_room_name(room):
    assert room.name == "Library"

def test_room_no_resident(empty_room):
    assert empty_room.resident_suspect is None

def test_room_starts_unsearched(room):
    assert room.searched is False

def test_room_starts_with_no_neighbours(room):
    assert room.neighbours == []

def test_room_starts_with_no_clues(room):
    assert room.clues == []


# ── connect() ─────────────────────────────────────────────────────────────────

def test_connect_adds_neighbour(room):
    room.connect("Hall")
    assert "Hall" in room.neighbours

def test_connect_multiple_neighbours(room):
    room.connect("Hall", "Kitchen", "Lounge")
    assert len(room.neighbours) == 3

def test_connect_no_duplicates(room):
    room.connect("Hall")
    room.connect("Hall")
    assert room.neighbours.count("Hall") == 1


# ── is_adjacent() ─────────────────────────────────────────────────────────────

def test_is_adjacent_true(room):
    room.connect("Hall")
    assert room.is_adjacent("Hall") is True

def test_is_adjacent_false(room):
    assert room.is_adjacent("Kitchen") is False


# ── add_clue() / search() ─────────────────────────────────────────────────────

def test_add_clue(room, clue):
    room.add_clue(clue)
    assert clue in room.clues

def test_search_returns_undiscovered_clues(room, clue):
    room.add_clue(clue)
    found = room.search()
    assert clue in found

def test_search_marks_clues_as_discovered(room, clue):
    room.add_clue(clue)
    room.search()
    assert clue.discovered is True

def test_search_second_time_returns_empty(room, clue):
    room.add_clue(clue)
    room.search()
    found_again = room.search()
    assert found_again == []

def test_search_sets_searched_flag(room, clue):
    room.add_clue(clue)
    room.search()
    assert room.searched is True


# ── get_resident_info() ───────────────────────────────────────────────────────

def test_get_resident_info_with_suspect(room):
    info = room.get_resident_info()
    assert "Professor Plum" in info

def test_get_resident_info_without_suspect(empty_room):
    info = empty_room.get_resident_info()
    assert "Nobody" in info


# ── Magic methods ─────────────────────────────────────────────────────────────

def test_len_no_clues(room):
    assert len(room) == 0

def test_len_with_clues(room, clue):
    room.add_clue(clue)
    assert len(room) == 1

def test_contains_clue(room, clue):
    room.add_clue(clue)
    assert clue in room

def test_str_returns_name(room):
    assert str(room) == "Library"

def test_repr(room):
    assert "Library" in repr(room)


# ── SecretPassage ─────────────────────────────────────────────────────────────

def test_secret_passage_leads_to(passage):
    assert passage.leads_to == "Kitchen"

def test_secret_passage_inherits_room(passage):
    assert isinstance(passage, Room)

def test_secret_passage_get_resident_info_mentions_passage(passage):
    info = passage.get_resident_info()
    assert "Kitchen" in info

def test_secret_passage_repr(passage):
    assert "Wine Cellar" in repr(passage)
    assert "Kitchen" in repr(passage)
