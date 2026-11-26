# Lab 7 — AI-Enhanced Interactive Text Adventure (CS 212)

## Project Name

**The Living Sunstone Text Adventure**

## Overview

This game is based on a book I wrote in 3rd grade. When I was around 22, I ended up rewriting a lot of it to actually have it make sense and so it sounded like an adult wrote it. I ended up writing a summary of the book during that time and after a while of working on the project in general, I stopped.

So now, I used the summary that I had written and turned it into a 10 leveled interaction choose your own adventure game.

## How I Used AI

I used Generative AI to help me write my `SPECS.md` file which I then used to give my AI Assisted Agent with more information to help actually write the code for the game.

In general, I used AI to help me with most things for this project. It helped me write the code for the game. It helped me break down my summary and turn it into the `story.json` file which includes the story content and choices. It generated the choices and interactions from each choice based off of my summary.

## To run the game:

You will need **Python 3.10+** and an **OpenRouter API key**.

### 1. Clone the Repository

```
git clone https://github.com/ZachoBeans/Lab-7-CS212.git
cd Lab-7-CS212
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```
python3 -m venv .venv
source .venv/bin/activate
```

> Using [uv](https://docs.astral.sh/uv/)? You can skip this step — `uv sync` in step 3 creates the `.venv` for you.

### 3. Install Dependencies

The project's dependencies are listed in `pyproject.toml`. Install them with either:

```
pip install openai python-dotenv
```

or, if you use uv:

```
uv sync
```

### 4. Configure Your API Key

Create a `.env` file in the project root directory (this file is gitignored and should never be committed) and add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

You can generate a free API key at [openrouter.ai](https://openrouter.ai/).

### 5. Run the Game

```
python the_living_sunstone.py
```

or, with uv:

```
uv run the_living_sunstone.py
```

## How to Play

After you run the game, you will be prompted to either start a new game, continue a current game, or quit.

1. Read the current scene description displayed in the terminal.

2. Type what you want your character to do in plain English (e.g., *"I kick the door down"* or *"I look around for a quiet way past"*). No options are shown; the AI matches your action to one of the story's hidden choices.

3. Wait a moment while the AI interprets your action and narrates the outcome.

4. Continue making choices until you reach one of the story's endings—or type `exit` at any prompt to return to the main menu.

Current games are saved automatically to `save.json` after each choice you make. If you choose **Continue** from the main menu, you will be returned to the last interaction you were on.

## Running the Unit Tests

From the project folder (with your `.venv` activated):

```
python -m unittest -v
```

or, with uv:

```
uv run python -m unittest -v
```

The tests live in the `tests/` folder. They replace the AI with a fake, so they never call OpenRouter (no API key or internet needed) and never touch your real `save.json`.

## Configuration & Troubleshooting

* **Changing the LLM Model:** Open `ai_request.py` and update the `MODEL` constant to any model ID available on [openrouter.ai/models](https://openrouter.ai/models).

* **`ModuleNotFoundError: No module named 'dotenv'`:** Make sure your `.venv` is activated and that you installed `python-dotenv` (not `dotenv`).

* **`Missing OPENROUTER_API_KEY in .env file`:** Make sure your `.env` file is in the project root folder and the key name is spelled exactly `OPENROUTER_API_KEY`.

## Author

**Zach Snyder** ([@ZachoBeans](https://github.com/ZachoBeans)) — CS 212, Lab 7

*Plan, ideas, and some implementations created by Zach Snyder with assistance from AI for code generation.*
