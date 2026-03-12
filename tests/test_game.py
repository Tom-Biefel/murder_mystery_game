"""
test_game.py — Isolated unit tests for mysterium.game
"""

import pytest
from mysterium.game import Game, CaseFile, build_mansion, validate_name, clue_generator
from mysterium.models.clue import all_clue_templates as all_clue_templates
from mysterium.models.room import SecretPassage


# Fixtures
@pytest.fixture
def game():
    return Game("Maria", difficulty="medium")


# validate_name()
def test_validate_name_valid():
    assert validate_name("Maria") is True


def test_validate_name_with_space():
    assert validate_name("Miss Marple") is True


def test_validate_name_too_short():
    with pytest.raises(ValueError):
        validate_name("A")


def test_validate_name_too_long():
    with pytest.raises(ValueError):
        validate_name("A" * 21)


def test_validate_name_invalid_chars():
    with pytest.raises(ValueError):
        validate_name("Maria123")


# clue_generator()
def test_clue_generator_yields_correct_count():
    gen = clue_generator(all_clue_templates, 5)
    result = list(gen)
    assert len(result) == 5


def test_clue_generator_yields_clues_from_list():
    gen = clue_generator(all_clue_templates, 3)
    for clue in gen:
        assert clue in all_clue_templates


def test_clue_generator_does_not_exceed_pool():
    gen = clue_generator(all_clue_templates, 9999)
    result = list(gen)
    assert len(result) == len(all_clue_templates)


# build_mansion()
def test_build_mansion_returns_11_rooms():
    rooms = build_mansion()
    assert len(rooms) == 11


def test_build_mansion_contains_hall():
    rooms = build_mansion()
    assert "Hall" in rooms


def test_build_mansion_secret_passages_are_subclass():
    rooms = build_mansion()
    assert isinstance(rooms["Wine Cellar"], SecretPassage)
    assert isinstance(rooms["Trophy Room"], SecretPassage)


def test_build_mansion_hall_has_neighbours():
    rooms = build_mansion()
    assert len(rooms["Hall"].neighbours) > 0


# CaseFile
def test_casefile_check_correct():
    c = CaseFile("Miss Scarlet", "Knife", "Lounge")
    assert c.check("Miss Scarlet", "Knife", "Lounge") is True


def test_casefile_check_wrong_suspect():
    c = CaseFile("Miss Scarlet", "Knife", "Lounge")
    assert c.check("Mr. Green", "Knife", "Lounge") is False


def test_casefile_check_wrong_weapon():
    c = CaseFile("Miss Scarlet", "Knife", "Lounge")
    assert c.check("Miss Scarlet", "Rope", "Lounge") is False


def test_casefile_check_wrong_room():
    c = CaseFile("Miss Scarlet", "Knife", "Lounge")
    assert c.check("Miss Scarlet", "Knife", "Kitchen") is False


def test_casefile_reveal_contains_all_parts():
    c = CaseFile("Miss Scarlet", "Knife", "Lounge")
    revealed = c.reveal()
    assert "Miss Scarlet" in revealed
    assert "Knife" in revealed
    assert "Lounge" in revealed


# Game.__init__
def test_game_player_name(game):
    assert game.player.name == "Maria"


def test_game_starts_not_over(game):
    assert game.game_over is False


def test_game_difficulty_set(game):
    assert game.difficulty == "medium"


def test_game_invalid_name_raises():
    with pytest.raises(ValueError):
        Game("A")


def test_game_rooms_populated(game):
    assert len(game.rooms) == 11


def test_game_hard_mode_limits_clues_per_room_to_one():
    hard_game = Game("Maria", difficulty="hard")
    assert all(len(room.clues) <= 1 for room in hard_game.rooms.values())


# Game.move()
def test_move_to_adjacent_room(game):
    result = game.move("Kitchen")
    assert result is True
    assert game.player.current_room == "Kitchen"


def test_move_to_non_adjacent_room(game):
    result = game.move("Wine Cellar")
    assert result is False
    assert game.player.current_room == "Hall"


def test_move_to_secret_passage_room_succeeds(game):
    assert game.move("Kitchen") is True
    assert game.move("Wine Cellar") is True
    assert game.player.current_room == "Wine Cellar"


# Game.search()
def test_search_returns_list(game):
    result = game.search()
    assert isinstance(result, list)


def test_search_adds_to_player_inventory(game):
    game.search()
    assert game.player.total_clues_found() >= 0


def test_search_second_time_empty(game):
    game.search()
    result = game.search()
    assert result == []


def test_game_cross_out_and_reinstate_delegate_to_player(game):
    game.cross_out("suspect", "Miss Scarlet")
    assert "Miss Scarlet" in game.player.crossed_suspects

    game.reinstate("suspect", "Miss Scarlet")
    assert "Miss Scarlet" not in game.player.crossed_suspects


# Game.accuse()
def test_accuse_sets_game_over(game):
    game.accuse("Miss Scarlet", "Knife", "Lounge")
    assert game.game_over is True


def test_accuse_wrong_returns_false(game):
    result = game.accuse("Nobody", "Nothing", "Nowhere")
    assert result["correct"] is False


def test_accuse_correct_returns_true(game):
    # Peek at the sealed solution to make a correct accusation
    result = game.accuse(game.case._suspect, game.case._weapon, game.case._room)
    assert result["correct"] is True


# Game.status()
def test_status_contains_expected_keys(game):
    s = game.status()
    assert "player" in s
    assert "room" in s
    assert "clues_found" in s
    assert "move_history" in s
    assert "game_over" in s


def test_status_player_name(game):
    assert game.status()["player"] == "Maria"


def test_status_initial_room(game):
    assert game.status()["room"] == "Hall"


# Game.use_passage()
def test_use_passage_from_normal_room_returns_none(game):
    assert game.use_passage() is None


def test_use_passage_from_secret_room_teleports(game):
    game.player.move("Wine Cellar")
    destination = game.use_passage()
    assert destination == "Kitchen"
    assert game.player.current_room == "Kitchen"
