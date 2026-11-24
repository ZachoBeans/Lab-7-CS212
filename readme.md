# Lab 7 — AI-Enhanced Interactive Text Adventure (CS 212)

## To run the game:

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

### 3. Install Dependencies

Install the required packages directly:

```
pip install openai python-dotenv

```

### 4. Configure Your API Key

Create a `.env` file in the project root directory (this file is gitignored and should never be committed) and add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here

```

You can generate a free API key at [openrouter.ai](https://openrouter.ai/).

### 5. Run the Game

```
python main.py

```

## How to Play

1. Read the current scene description displayed in the terminal.

2. Type what you want your character to do in plain English (e.g., *"I kick the door down"* or *"I look around for a quiet way past"*).

3. Wait a moment while the AI interprets your action and narrates the outcome.

4. Continue making choices until you reach one of the story's endings—or type `exit` at any prompt to quit.

## Configuration & Troubleshooting

* **Changing the LLM Model:** Open `request.py` and update the `MODEL` constant to any model ID available on [openrouter.ai/models](https://openrouter.ai/models).

* **`ModuleNotFoundError: No module named 'dotenv'`:** Make sure your `.venv` is activated and that you installed `python-dotenv` (not `dotenv`).

## Author

**Zach Snyder** ([@ZachoBeans](https://github.com/ZachoBeans)) — CS 212, Lab 7