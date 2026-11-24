# Lab 6 CS212 - Zach Snyder - 11/15/26

# -- Project Name --
# The Living Sunstone Text Adventure

# -- Overview --
# This game is based on a book I wrote in 3rd grade. When I was around 22, I ended up rewriting a lot of it to actually have it make sense
# and so it sounded like an adult wrote it. I ended up writing a summary of the book during that time and after a while of working on the
# project in general, I stopped.

# So now, I used the summary that I had written and turned it into a 10 leveled interaction choose your own adventure game.

# -- How I Used AI --
# I used Generative AI to help me write my SPECS.md file which I then used to give my AI Assited Agent with more information to help
# actually write the code for the game.

# In general, I used AI to help me with most things for this project. It helped me write the code for the game. It helped me break down my
# summary and turn it into the story.json file which includes the story content and choices. It generated the choices and interactions
# from each choice based off of my summary.

# -- How to Play --
# The game is played by typing what you want to do. No options are shown; the AI matches your action to one of the story's hidden choices. After you run the game, you will be prompted to either start a new game, continue a current game, or quit. Current games
# are saved automatically after each choice you make. If you type 'exit' during an interaction,
# it will return you to the main menu. If you press continue, at that point, you will be returned to your last interaction you were on.

# -- How to Run --
# To run the game, you will need to have Python 3 installed on your computer
# After that, you can run the game by using the terminal and running the command `python the_living_sunstone.py`

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STORY_PATH = ROOT / "story.json"
SAVE_PATH = ROOT / "save.json"

PROMPT = "What will you do? (Type 'exit' to quit): "

# ai_request.py reads .env relative to the working directory, so run from the project folder.
os.chdir(ROOT)
# The LLM often returns characters like em dashes; make sure the console can print them.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
try:
    from ai_request import resolve_player_action
except Exception as exc:  # missing package, missing API key, etc.
    resolve_player_action = None
    AI_ERROR = str(exc)
else:
    AI_ERROR = None


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_story():
    try:
        with STORY_PATH.open(encoding="utf-8") as handle:
            story = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Could not read {STORY_PATH.name}: {exc}")
        sys.exit(1)

    if "start" not in story or not isinstance(story, dict):
        print("story.json is missing a 'start' node.")
        sys.exit(1)
    return story


def save_game(node_id, turn_count):
    payload = {"current_node": node_id, "turn_count": turn_count}
    with SAVE_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def clear_save():
    if SAVE_PATH.exists():
        SAVE_PATH.unlink()


def load_save(story):
    if not SAVE_PATH.exists():
        return None, "No save file found. Start a new game first."

    try:
        with SAVE_PATH.open(encoding="utf-8") as handle:
            data = json.load(handle)
        node_id = data["current_node"]
        turn_count = data["turn_count"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return None, "The save file is unreadable. Start a new game."

    if node_id not in story or not isinstance(turn_count, int) or turn_count < 0:
        return None, "The save file does not match this story. Start a new game."

    return (node_id, turn_count), None


def read_choice(prompt, valid):
    while True:
        raw = input(prompt).strip()
        if raw in valid:
            return int(raw)
        print("Enter " + ", ".join(valid[:-1]) + f", or {valid[-1]}.")


def show_ending(node):
    print(node.get("title", "Ending"))
    print("=" * len(node.get("title", "Ending")))
    print()
    print(node["text"])
    print()
    input("Press Enter to return to the main menu.")


def play(story, node_id, turn_count):
    while True:
        node = story[node_id]
        save_game(node_id, turn_count)
        clear_screen()

        if node.get("ending"):
            show_ending(node)
            clear_save()
            return

        choices = node.get("choices") or []
        if len(choices) != 3:
            print("This story node is missing its three choices.")
            input("Press Enter to return to the main menu.")
            return

        interaction = turn_count + 1
        print(f"[Interaction {interaction}/10]")
        print()
        print(node["text"])
        print()

        while True:
            raw = input(PROMPT).strip()
            if raw.lower() == "exit":
                return
            if not raw:
                continue
            if resolve_player_action is None:
                print(f"Free-text actions are unavailable ({AI_ERROR}).")
                continue

            print("Thinking...")
            options = {str(i): c["text"] for i, c in enumerate(choices, start=1)}
            result = resolve_player_action(node["text"], options, raw)
            if not isinstance(result, dict):
                result = {}
            matched = result.get("matched_choice_id")
            print()
            print(result.get("custom_narration") or "The earpiece crackles but says nothing useful. Try again.")
            print()
            if matched is not None and str(matched).strip() in options:
                matched = str(matched).strip()
                input("Press Enter to continue.")
                selected = int(matched)
                break

        node_id = choices[selected - 1]["next_node"]
        turn_count += 1

        if node_id not in story:
            print("The story has no path by that name. Returning to the menu.")
            input("Press Enter to continue.")
            return


def show_menu():
    clear_screen()
    print("=" * 46)
    print("  DIMENSIONAL RIFT: The Living Sunstone")
    print("=" * 46)
    print()
    print("Bob, a scientist for Transdimensional Solutions,")
    print("is stranded after a Jump Portal test. Ten choices")
    print("stand between him and the way home.")
    print()
    print("1. Start New Game")
    print("2. Continue")
    print("3. Quit")
    print()


def main():
    story = load_story()

    while True:
        show_menu()
        option = read_choice("Select an option (1/2/3): ", ("1", "2", "3"))

        if option == 1:
            clear_save()
            play(story, "start", 0)
        elif option == 2:
            loaded, error = load_save(story)
            if error:
                print()
                print(error)
                input("Press Enter to return to the main menu.")
                continue
            node_id, turn_count = loaded
            play(story, node_id, turn_count)
        else:
            clear_screen()
            print("The rift closes. Goodbye.")
            return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("The rift closes. Goodbye.")
