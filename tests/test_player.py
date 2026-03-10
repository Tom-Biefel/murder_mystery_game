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
    return Clue("A red ribbon", "Miss Scarlet", 0.8)


# __init__
def test_player_default_start_room(player):
    assert player.current_room == "Hall"


def test_player_custom_start_room():
    p = Player("Bob", start_room="Kitchen")
    assert p.current_room == "Kitchen"


def test_player_initial_inventory_empty(player):
    assert player.inventory == []


def test_player_initial_evidence_empty(player):
    assert player.evidence == {}


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


def test_collect_clue_updates_evidence(player, clue):
    player.collect_clue(clue)
    assert "Miss Scarlet" in player.evidence


def test_collect_clue_accumulates_weight(player):
    c1 = Clue("Clue A", "Professor Plum", 0.6)
    c2 = Clue("Clue B", "Professor Plum", 0.4)
    player.collect_clue(c1)
    player.collect_clue(c2)
    assert player.evidence["Professor Plum"] == pytest.approx(1.0)


# total_clues_found()
def test_total_clues_found_starts_at_zero(player):
    assert player.total_clues_found() == 0


def test_total_clues_found_counts_correctly(player, clue):
    player.collect_clue(clue)
    assert player.total_clues_found() == 1


# evidence_summary()
def test_evidence_summary_empty(player):
    assert player.evidence_summary() == {}


def test_evidence_summary_sums_to_100(player):
    player.collect_clue(Clue("A", "Scarlet", 0.5))
    player.collect_clue(Clue("B", "Plum", 0.5))
    summary = player.evidence_summary()
    assert sum(summary.values()) == pytest.approx(100.0)


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
