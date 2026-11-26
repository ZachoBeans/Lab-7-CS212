# Plan, ideas, and some implementations created by Zach Snyder with assistance from AI for code generation

"""Unit tests for the game logic in the_living_sunstone.py.

Run from the project folder with:  python -m unittest
None of these tests call the real AI or touch the real save.json.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import the_living_sunstone as game


class StoryFileTests(unittest.TestCase):
    """Checks that the real story.json is valid and follows the SPECS rules."""

    @classmethod
    def setUpClass(cls):
        cls.story = game.load_story()

    def test_story_has_start_node(self):
        self.assertIn("start", self.story)

    def test_every_non_ending_node_has_three_choices(self):
        for node_id, node in self.story.items():
            if node.get("ending"):
                continue
            with self.subTest(node=node_id):
                self.assertEqual(len(node.get("choices", [])), 3)

    def test_every_choice_points_to_a_real_node(self):
        for node_id, node in self.story.items():
            for choice in node.get("choices", []):
                with self.subTest(node=node_id, choice=choice["text"]):
                    self.assertIn(choice["next_node"], self.story)

    def test_every_node_has_story_text(self):
        for node_id, node in self.story.items():
            with self.subTest(node=node_id):
                self.assertTrue(node.get("text", "").strip())

    def test_at_least_one_ending_exists(self):
        self.assertTrue(any(node.get("ending") for node in self.story.values()))


class SaveFileTests(unittest.TestCase):
    """Tests save_game, load_save, and clear_save using a temporary save file."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.save_path = Path(self.tmp.name) / "save.json"
        patcher = mock.patch.object(game, "SAVE_PATH", self.save_path)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)
        self.story = {"start": {"text": "x"}, "next": {"text": "y"}}

    def test_save_then_load_round_trip(self):
        game.save_game("next", 4)
        loaded, error = game.load_save(self.story)
        self.assertIsNone(error)
        self.assertEqual(loaded, ("next", 4))

    def test_load_with_no_save_file(self):
        loaded, error = game.load_save(self.story)
        self.assertIsNone(loaded)
        self.assertIn("No save file", error)

    def test_load_with_corrupt_json(self):
        self.save_path.write_text("{not json", encoding="utf-8")
        loaded, error = game.load_save(self.story)
        self.assertIsNone(loaded)
        self.assertIn("unreadable", error)

    def test_load_with_unknown_node(self):
        game.save_game("missing_node", 2)
        loaded, error = game.load_save(self.story)
        self.assertIsNone(loaded)
        self.assertIn("does not match", error)

    def test_load_with_negative_turn_count(self):
        self.save_path.write_text(
            json.dumps({"current_node": "start", "turn_count": -1}), encoding="utf-8"
        )
        loaded, error = game.load_save(self.story)
        self.assertIsNone(loaded)

    def test_clear_save_removes_file(self):
        game.save_game("start", 0)
        game.clear_save()
        self.assertFalse(self.save_path.exists())

    def test_clear_save_without_file_does_not_crash(self):
        game.clear_save()
        self.assertFalse(self.save_path.exists())


class ReadChoiceTests(unittest.TestCase):
    """Tests the menu input validation."""

    @mock.patch("builtins.print")
    @mock.patch("builtins.input", side_effect=["9", "abc", "", "2"])
    def test_reprompts_until_valid(self, mock_input, _print):
        result = game.read_choice("> ", ("1", "2", "3"))
        self.assertEqual(result, 2)
        self.assertEqual(mock_input.call_count, 4)

    @mock.patch("builtins.input", return_value=" 3 ")
    def test_strips_whitespace(self, _input):
        self.assertEqual(game.read_choice("> ", ("1", "2", "3")), 3)


class PlayTests(unittest.TestCase):
    """Tests the main game loop with the AI replaced by a fake."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.save_path = Path(self.tmp.name) / "save.json"
        for patcher in (
            mock.patch.object(game, "SAVE_PATH", self.save_path),
            mock.patch.object(game, "clear_screen"),
            mock.patch("builtins.print"),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(self.tmp.cleanup)

        self.story = {
            "start": {
                "text": "Start scene.",
                "choices": [
                    {"text": "Go left", "next_node": "end_left"},
                    {"text": "Go right", "next_node": "end_right"},
                    {"text": "Stay", "next_node": "start"},
                ],
            },
            "end_left": {"ending": True, "title": "Left Ending", "text": "You went left."},
            "end_right": {"ending": True, "title": "Right Ending", "text": "You went right."},
        }

    def test_exit_returns_to_menu_and_keeps_save(self):
        with mock.patch("builtins.input", return_value="exit"):
            game.play(self.story, "start", 0)
        data = json.loads(self.save_path.read_text(encoding="utf-8"))
        self.assertEqual(data, {"current_node": "start", "turn_count": 0})

    def test_ai_match_moves_to_next_node_and_reaching_ending_clears_save(self):
        fake_ai = mock.Mock(
            return_value={"matched_choice_id": "2", "custom_narration": "You head right."}
        )
        with mock.patch.object(game, "resolve_player_action", fake_ai), mock.patch(
            "builtins.input", side_effect=["walk to the right", "", ""]
        ):
            game.play(self.story, "start", 0)

        fake_ai.assert_called_once()
        _scene, options, action = fake_ai.call_args.args
        self.assertEqual(options, {"1": "Go left", "2": "Go right", "3": "Stay"})
        self.assertEqual(action, "walk to the right")
        # The ending was reached, so the save file should be gone.
        self.assertFalse(self.save_path.exists())

    def test_ai_returning_no_match_asks_again(self):
        fake_ai = mock.Mock(
            side_effect=[
                {"matched_choice_id": None, "custom_narration": "That makes no sense."},
                {"matched_choice_id": "1", "custom_narration": "You go left."},
            ]
        )
        with mock.patch.object(game, "resolve_player_action", fake_ai), mock.patch(
            "builtins.input", side_effect=["fly to the moon", "go left", "", ""]
        ):
            game.play(self.story, "start", 0)
        self.assertEqual(fake_ai.call_count, 2)

    def test_ai_returning_invalid_choice_id_is_ignored(self):
        fake_ai = mock.Mock(
            return_value={"matched_choice_id": "7", "custom_narration": "Huh?"}
        )
        with mock.patch.object(game, "resolve_player_action", fake_ai), mock.patch(
            "builtins.input", side_effect=["do something", "exit"]
        ):
            game.play(self.story, "start", 0)
        # Still on the start node because "7" is not a valid choice.
        data = json.loads(self.save_path.read_text(encoding="utf-8"))
        self.assertEqual(data["current_node"], "start")

    def test_turn_counter_increases_after_a_choice(self):
        fake_ai = mock.Mock(
            return_value={"matched_choice_id": "3", "custom_narration": "You wait."}
        )
        with mock.patch.object(game, "resolve_player_action", fake_ai), mock.patch(
            "builtins.input", side_effect=["wait here", "", "exit"]
        ):
            game.play(self.story, "start", 0)
        data = json.loads(self.save_path.read_text(encoding="utf-8"))
        self.assertEqual(data, {"current_node": "start", "turn_count": 1})


if __name__ == "__main__":
    unittest.main()
