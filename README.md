# Mysterium — Murder Mystery Game

A digital murder mystery game inspired by **Clue/Cluedo**, built with Python.
Explore Blackwood Manor, collect clues, and accuse the right suspect before it's too late.

---

## Features

- 11 rooms to explore including secret passages
- 6 suspects, 6 weapons, randomised solution every game
- Evidence tracking with weighted clues
- CLI interface for terminal play
- Streamlit UI (coming soon)
- 128 unit tests with full coverage

---

## Installation

### From TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mysterium
```

### Local Development

```bash
git clone <repo-url>
cd murder_mystery_game
uv sync
```

---

## Usage

```bash
streamlit run src/mysterium/app.py
```

**Difficulty options:** `easy` · `medium` · `hard`

---

## Project Structure

```
src/mysterium/
├── game.py          # Game engine (Game, CaseFile, build_mansion)
└── models/
    ├── clue.py      # Clue class + all_clue_templates
    ├── player.py    # Player class
    ├── room.py      # Room + SecretPassage
    ├── suspect.py   # Suspect class + all_suspects
    └── weapon.py    # Weapon class + all_weapons

tests/
├── test_clue.py
├── test_player.py
├── test_room.py
├── test_suspect.py
├── test_weapon.py
└── test_game.py
```

---

## Running Tests

```bash
# All tests
python -m pytest tests/ -v

# With coverage report
python -m pytest --cov=src/mysterium --cov-report=term-missing
```

---

## Suspects

| Suspect | Color | Home Room |
|---|---|---|
| Miss Scarlet | Red | Lounge |
| Colonel Mustard | Yellow | Billiard Room |
| Mrs. Peacock | Blue | Conservatory |
| Professor Plum | Purple | Library |
| Mr. Green | Green | Study |
| Mrs. White | White | Kitchen |

---

## Weapons

Candlestick · Knife · Lead Pipe · Revolver · Rope · Wrench

---

## Requirements

- Python >= 3.13
- python-dotenv
- streamlit
