"""
test_player.py — Isolated unit tests for mysterium.models.player
"""

import pytest
from mysterium.models.player import Player
from mysterium.models.clue import Clue


# Fixtures
@pytest.fixture
def player():
    return Player("Maria")


@pytest.fixture
def clue():
    return Clue("A red ribbon", "Miss Scarlet")


# __init__
def test_player_default_start_room(player):
    assert player.current_room == "Hall"


def test_player_custom_start_room():
    p = Player("Bob", start_room="Kitchen")
    assert p.current_room == "Kitchen"


def test_player_initial_inventory_empty(player):
    assert player.inventory == []


def test_player_initial_notebook_empty(player):
    state = player.notebook_state()
    assert state["crossed_suspects"] == set()
    assert state["crossed_weapons"] == set()
    assert state["crossed_rooms"] == set()


# move()
def test_move_changes_current_room(player):
    player.move("Kitchen")
    assert player.current_room == "Kitchen"


def test_move_logged_in_history(player):
    player.move("Library")
    assert player.move_history[-1][0] == "Library"


def test_move_history_max_10(player):
    for i in range(15):
        player.move(f"Room{i}")
    assert len(player.move_history) == 10


# collect_clue()
def test_collect_clue_adds_to_inventory(player, clue):
    player.collect_clue(clue)
    assert clue in player.inventory


def test_collect_clue_keeps_summary_points_to(player, clue):
    player.collect_clue(clue)
    summary = player.clues_summary()
    assert summary[0]["points_to"] == "Miss Scarlet"


def test_collect_clue_accumulates_inventory_count(player):
    c1 = Clue("Clue A", "Professor Plum")
    c2 = Clue("Clue B", "Professor Plum")
    player.collect_clue(c1)
    player.collect_clue(c2)
    assert len(player.inventory) == 2


# total_clues_found()
def test_total_clues_found_starts_at_zero(player):
    assert player.total_clues_found() == 0


def test_total_clues_found_counts_correctly(player, clue):
    player.collect_clue(clue)
    assert player.total_clues_found() == 1


# clues_summary()
def test_clues_summary_empty(player):
    assert player.clues_summary() == []


def test_clues_summary_contains_expected_fields(player):
    player.collect_clue(Clue("A", "Scarlet", "suspect"))
    summary = player.clues_summary()
    assert summary[0]["description"] == "A"
    assert summary[0]["points_to"] == "Scarlet"
    assert summary[0]["category"] == "suspect"


def test_cross_out_tracks_each_category(player):
    player.cross_out("suspect", "Miss Scarlet")
    player.cross_out("weapon", "Knife")
    player.cross_out("room", "Kitchen")

    state = player.notebook_state()
    assert "Miss Scarlet" in state["crossed_suspects"]
    assert "Knife" in state["crossed_weapons"]
    assert "Kitchen" in state["crossed_rooms"]


def test_cross_out_invalid_category_raises(player):
    with pytest.raises(ValueError):
        player.cross_out("pet", "Dog")


def test_reinstate_removes_each_category(player):
    player.cross_out("suspect", "Miss Scarlet")
    player.cross_out("weapon", "Knife")
    player.cross_out("room", "Kitchen")

    player.reinstate("suspect", "Miss Scarlet")
    player.reinstate("weapon", "Knife")
    player.reinstate("room", "Kitchen")

    state = player.notebook_state()
    assert "Miss Scarlet" not in state["crossed_suspects"]
    assert "Knife" not in state["crossed_weapons"]
    assert "Kitchen" not in state["crossed_rooms"]


def test_reinstate_invalid_category_raises(player):
    with pytest.raises(ValueError):
        player.reinstate("pet", "Dog")


# add_note()
def test_add_note_stores_text(player):
    player.add_note("Suspicious footprints.")
    assert any("Suspicious footprints." in note for note in player.notes)


def test_add_note_multiple(player):
    player.add_note("Note 1")
    player.add_note("Note 2")
    assert len(player.notes) == 2


# Magic methods
def test_repr_contains_name(player):
    assert "Maria" in repr(player)


def test_str_contains_name(player):
    assert "Maria" in str(player)
