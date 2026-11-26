# Plan, ideas, and some implementations created by Zach Snyder with assistance from AI for code generation

"""Unit tests for ai_request.py.

The real OpenRouter API is never called: the client is replaced with a fake
that returns whatever text each test needs. A fake API key is supplied too,
so these tests work even without a .env file.
"""

import importlib
import sys
import unittest
from types import SimpleNamespace
from unittest import mock


def import_ai_request():
    """Import ai_request with a fake API key so no real .env is needed."""
    sys.modules.pop("ai_request", None)
    with mock.patch("dotenv.dotenv_values", return_value={"OPENROUTER_API_KEY": "test-key"}):
        return importlib.import_module("ai_request")


def fake_response(text):
    """Build an object shaped like an OpenAI chat completion response."""
    message = SimpleNamespace(content=text)
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


class ResolvePlayerActionTests(unittest.TestCase):
    def setUp(self):
        self.ai = import_ai_request()
        self.fake_client = mock.Mock()
        patcher = mock.patch.object(self.ai, "client", self.fake_client)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.choices = {"1": "Open the door", "2": "Run away"}

    def reply_with(self, text):
        self.fake_client.chat.completions.create.return_value = fake_response(text)

    def test_parses_plain_json(self):
        self.reply_with('{"matched_choice_id": "1", "custom_narration": "You open it."}')
        result = self.ai.resolve_player_action("A door.", self.choices, "open door")
        self.assertEqual(result["matched_choice_id"], "1")
        self.assertEqual(result["custom_narration"], "You open it.")

    def test_strips_markdown_code_fences(self):
        self.reply_with('```json\n{"matched_choice_id": "2", "custom_narration": "You flee."}\n```')
        result = self.ai.resolve_player_action("A door.", self.choices, "run")
        self.assertEqual(result["matched_choice_id"], "2")

    def test_invalid_json_returns_safe_fallback(self):
        self.reply_with("Sorry, I cannot help with that.")
        result = self.ai.resolve_player_action("A door.", self.choices, "???")
        self.assertIsNone(result["matched_choice_id"])
        self.assertTrue(result["custom_narration"])

    def test_empty_reply_returns_safe_fallback(self):
        self.reply_with(None)
        result = self.ai.resolve_player_action("A door.", self.choices, "hmm")
        self.assertIsNone(result["matched_choice_id"])

    def test_connection_error_returns_safe_fallback(self):
        self.fake_client.chat.completions.create.side_effect = RuntimeError("offline")
        result = self.ai.resolve_player_action("A door.", self.choices, "open door")
        self.assertIsNone(result["matched_choice_id"])
        self.assertIn("offline", result["custom_narration"])

    def test_prompt_includes_scene_choices_and_action(self):
        self.reply_with('{"matched_choice_id": "1", "custom_narration": "ok"}')
        self.ai.resolve_player_action("A heavy door.", self.choices, "kick it")
        kwargs = self.fake_client.chat.completions.create.call_args.kwargs
        user_message = kwargs["messages"][1]["content"]
        self.assertIn("A heavy door.", user_message)
        self.assertIn("Open the door", user_message)
        self.assertIn("kick it", user_message)
        self.assertEqual(kwargs["model"], self.ai.MODEL)


class MissingApiKeyTests(unittest.TestCase):
    def test_missing_key_raises_value_error(self):
        sys.modules.pop("ai_request", None)
        self.addCleanup(sys.modules.pop, "ai_request", None)
        with mock.patch("dotenv.dotenv_values", return_value={}):
            with self.assertRaises(ValueError):
                importlib.import_module("ai_request")


if __name__ == "__main__":
    unittest.main()
