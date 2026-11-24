import json
from dotenv import dotenv_values
from openai import OpenAI

MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

settings = dotenv_values(".env")
api_key = settings.get("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("Missing OPENROUTER_API_KEY in .env file.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

SYSTEM_PROMPT = """You are a narrative router for a text adventure game.
Given the current scene, a list of valid story choices, and what the player wants to do:
1. Pick the choice ID that best matches the player's intent/outcome.
2. Rewrite a short transition (2-3 sentences) that incorporates the player's exact action and leads naturally into that choice's outcome.
3. If the player's action is impossible or makes no sense in the scene, set "matched_choice_id" to null and explain why in-character.

Respond ONLY with valid JSON in this exact format:
{
  "matched_choice_id": "choice_id_or_null",
  "custom_narration": "Your adapted narrative transition here."
}
"""
def resolve_player_action(scene_text: str, choices: dict, user_input: str) -> dict:
    """Matches free-form player input to the closest valid JSON choice."""
    user_prompt = (
        f"CURRENT SCENE:\n{scene_text}\n\n"
        f"VALID CHOICES:\n{json.dumps(choices, indent=2)}\n\n"
        f"PLAYER ACTION:\n{user_input}"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        raw_text = (response.choices[0].message.content or "").strip()

        # Strip markdown code fences if the model wraps its JSON in ```json ... ```
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()

        return json.loads(raw_text)

    except json.JSONDecodeError:
        return {
            "matched_choice_id": None,
            "custom_narration": "You hesitate for a moment—try describing your action a little more clearly.",
        }
    except Exception as e:
        return {
            "matched_choice_id": None,
            "custom_narration": f"[AI connection error: {e}] Try again or pick a standard option.",
        }


# Only runs when you execute `python ai_request.py` directly, NOT when imported
if __name__ == "__main__":
    sample_scene = "You stand before a heavy iron door. A rusty lock holds it shut."
    sample_choices = {
        "force": "Break the door open loudly",
        "sneak": "Pick the lock quietly",
    }

    while True:
        action = input("\nWhat do you do? (or 'exit'): ").strip()
        if action.lower() == "exit":
            break
        if not action:
            continue

        print("Thinking...")
        result = resolve_player_action(sample_scene, sample_choices, action)
        print("Matched ID:", result.get("matched_choice_id"))
        print("Narration:", result.get("custom_narration"))