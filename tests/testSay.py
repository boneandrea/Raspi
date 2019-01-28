import perform
import unittest
import subprocess
import sqlite3

from unittest.mock import patch, MagicMock, call

DB_PROGRAM = "sqlite3"
DB_SCHEMA = "schema.sql"
TEST_DB = "test.db"


class TestSay(unittest.TestCase):

    conn = None

    def setUp(self):
        self._initDb()
        self.app = perform.Perform()
        self.app.init(TEST_DB)
        self.app.init_log()

    def tearDown(self):
        self.app.close()
        pass

    def _initDb(self):
        p = subprocess.Popen([DB_PROGRAM, TEST_DB], stdin=subprocess.PIPE)
        with open(DB_SCHEMA, "r") as f:
            data = f.read()
            p.communicate(data.encode())
        self.conn = sqlite3.connect(TEST_DB)
        pass
    #####

    def test_dequeue(self):
        # test to decrease by 1
        c = self.conn.cursor()
        c.execute('select count(*) from entries')
        data = self.app.dequeue()
        self.assertEqual(0, len(data))
        pass

    def test_enqueue(self):
        data = self.app.enqueue(title="TITLE", text="テキスト")
        self.assertEqual("テキスト", data["text"])
        self.assertIsNotNone(data)

    def test_led_message(self):
        self.assertTrue(self.app.led_message({"text": "my_text"}))

        with self.assertRaises(KeyError):  # 例外のテスト
            self.assertRaises(KeyError, self.app.led_message(
                {"text_not_exist": "my_text"}))

    def test_my_perform(self):
        self.assertTrue(self.app.my_perform({"text": "my_text"}))

    def test_mytrigger(self):
        self.assertTrue(type(self.app.mytrigger()) is list)

    def test_1action(self):
        mock_lib = MagicMock()
        with patch('Perform', return_value=mock_lib):
            Perform.mytrigger()
            assert mock_lib.dequeue.called is True
            # perform.enqueue(title="TITLE", text="テキスト")

    #     assert True is True
#        assert mock_lib.enqueue.called is True
        # perform.enqueue(title="TITLE", text="テキスト")
        # perform.dequeue()
        # self.assertIsNotNone(data)
