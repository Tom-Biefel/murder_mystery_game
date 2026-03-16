
# 🕯️ Mysterium: The Game Engine

This repository contains the **core Python package** for the murder mystery game *Mysterium: Blackwood Manor*.

The package implements the **game logic and data models**, including:

- Game engine
- Mansion map
- Clue system
- Suspects and weapons
- Player logic
- Unit tests

The playable interface is provided by a separate **Streamlit application**.

---

# Play the Game

The interactive web version of the game is available in the Streamlit repository:

https://github.com/Tom-Biefel/mysterium-app

That application installs this package and provides the graphical interface.

---

# Package Purpose

This repository provides the reusable Python package:

```
mysterium
```

It demonstrates several Python programming concepts including object-oriented design, generators, decorators, and automated testing.

---

# Python Concepts Demonstrated

The project showcases the following Python concepts:

### Object-Oriented Programming
- Classes and instances
- Composition (`Game` contains `Player`, `Room`, and `CaseFile`)
- Inheritance (`SecretPassage` extends `Room`)

### Decorators
`@log_action` logs player movement with timestamps.

### Generators
`clue_generator()` yields clues lazily when distributing them across rooms.

### Regular Expressions
Player names are validated using the `re` module.

### Environment Variables
`.env` configuration is loaded using `python-dotenv`.

### Collections
`deque` is used to store player movement history.

### Testing
Comprehensive unit tests are implemented using `pytest`.

---

# Installation

## Install from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ \
--extra-index-url https://pypi.org/simple/ mysterium
```

---

## Install Locally (Development)

Requirements:

- Python **3.13+**
- **uv** package manager

Clone the repository:

```bash
git clone https://github.com/Tom-Biefel/murder_mystery_game.git
cd murder_mystery_game
```

Install dependencies:

```bash
uv sync
uv pip install -e .
```

---

# Running Tests

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov
```

---

# Project Structure

```
src/mysterium/
├── game.py          # Game engine and orchestration
└── models/
    ├── clue.py      # Clue class and clue definitions
    ├── player.py    # Player class and notebook logic
    ├── room.py      # Room and SecretPassage classes
    ├── suspect.py   # Suspect class and all suspects
    └── weapon.py    # Weapon class and all weapons

tests/
├── test_game.py
├── test_clue.py
├── test_player.py
├── test_room.py
├── test_suspect.py
└── test_weapon.py
```

---

# Related Repository

Streamlit game interface:

https://github.com/Tom-Biefel/mysterium-app

This application installs the `mysterium` package and provides the graphical interface for playing the game.

---

# Architecture

```
murder_mystery_game (Python package)
        ↓
mysterium-app (Streamlit UI)
```

The **package repository** contains the reusable game engine.

The **Streamlit repository** provides the user interface and imports the package as a dependency.

