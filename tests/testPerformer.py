import performer
import unittest
import subprocess

from unittest.mock import patch, MagicMock, call

class TestPerformer(unittest.TestCase):
    conn = None

    def setUp(self):
        self.app = performer.Performer()

    def tearDown(self):
        pass

    def test_led_message(self):
        self.assertTrue(self.app.led_message({"text": "my_text"}))

        with self.assertRaises(KeyError):  # 例外のテスト
            self.assertRaises(KeyError, self.app.led_message(
                {"text_not_exist": "my_text"}))

    def test_say(self):
        self.assertTrue(self.app.say({"text": "my_text"}))

        with self.assertRaises(KeyError):  # 例外のテスト
            self.assertRaises(KeyError, self.app.say(
                {"text_not_exist": "my_text"}))
