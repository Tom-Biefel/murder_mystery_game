"""
cli.py — Command-line interface for Mysterium.

Python concepts: argparse, while loops, scripts/entry points, docstrings

Registered in pyproject.toml so users can run: mysterium --name Maria
"""

import argparse
from mysterium.game import Game


def main():
    """Entry point for the CLI. Registered as 'mysterium' in pyproject.toml."""

    # argparse — defines --name and --difficulty command-line arguments
    parser = argparse.ArgumentParser(description="Mysterium — Murder Mystery Game")
    parser.add_argument("--name",       type=str, default="Detective",
                        help="Your detective name")
    parser.add_argument("--difficulty", type=str, default="medium",
                        choices=["easy", "medium", "hard"],
                        help="Game difficulty")
    args = parser.parse_args()

    game = Game(player_name=args.name, difficulty=args.difficulty)
    print(f"\nWelcome, {args.name}! A murder has occurred at Blackwood Manor.")
    print("You start in the Hall. Commands: go <room> | search | accuse | status | quit\n")

    while not game.game_over:   # while loop — the entire game loop
        print(f"\n[Room: {game.player.current_room}] "
              f"[Clues: {game.player.total_clues_found}]")
        print(f"Exits: {', '.join(game.rooms[game.player.current_room].neighbours)}")
        cmd = input("> ").strip()

        if cmd.startswith("go "):
            room_name = cmd[3:].strip()
            game.move(room_name)

        elif cmd == "search":
            found = game.search()
            if found:
                for clue in found:
                    print(f"  Found: {clue}")
            else:
                print("  Nothing new found here.")

        elif cmd.startswith("accuse "):
            parts = cmd[7:].split(",")
            if len(parts) == 3:
                result = game.accuse(parts[0].strip(), parts[1].strip(), parts[2].strip())
                print(f"\n{result['message']}")
            else:
                print("  Format: accuse <suspect>, <weapon>, <room>")

        elif cmd == "status":
            print(game.status())

        elif cmd == "quit":
            print("Goodbye, detective.")
            break

        else:
            print("  Unknown command. Try: go <room> | search | accuse | status | quit")


if __name__ == "__main__":
    main()