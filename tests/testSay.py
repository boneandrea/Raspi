import popper
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
        self.conn = self._initDb()
        self.app = popper.Popper()
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
        return sqlite3.connect(TEST_DB)

    # </helper>

    def test_init(self):
        assert self.conn is not None

    def test_dequeue(self):
        mock_lib = MagicMock()
        with patch('performer.Performer', return_value=mock_lib):
            self.app.enqueue(title="TITLE", text="テキスト")
            data = self.app.dequeue()
            self.assertEqual(1, len(data))

            # test to be empty
            c = self.conn.cursor()
            c.execute('select * from entries')
            entries = c.fetchall()
            assert len(entries) == 0

    def test_enqueue0(self):
        data = self.app.enqueue(title="TITLE", text="テキスト")
        self.assertEqual("テキスト", data["text"])
        self.assertIsNotNone(data)

        qdata = self.app.dequeue()[0]
        assert qdata["led"] == 1
        assert qdata["voice"] == 1

    def test_enqueue1(self):
        data = self.app.enqueue(title="TITLE", text="テキスト", led=False)
        self.assertEqual("テキスト", data["text"])
        self.assertIsNotNone(data)

        qdata = self.app.dequeue()[0]
        assert qdata["led"] == 0
        assert qdata["voice"] == 1

    def test_enqueue1(self):
        data = self.app.enqueue(title="TITLE", text="テキスト", voice=False)
        self.assertEqual("テキスト", data["text"])
        self.assertIsNotNone(data)

        qdata = self.app.dequeue()[0]
        assert qdata["led"] == 1
        assert qdata["voice"] == 0

    def test_mytrigger(self):
        self.assertTrue(type(self.app.mytrigger()) is list)

    def test_mock_action(self):
        mock_lib = MagicMock()
        with patch('mock.MyMock', return_value=mock_lib):
            self.app.mytrigger()
            assert mock_lib.hello.called is True

    def test_perform0(self):
        mock_lib = MagicMock()
        with patch('performer.Performer', return_value=mock_lib):
            self.app.my_perform({
                "text": "my_text",
                "voice": True,
                "led": True
            })
            assert mock_lib.led_message.called is True
            assert mock_lib.say.called is True
            mock_lib.say.assert_called()
            mock_lib.say.assert_called_once()
            mock_lib.led_message.assert_called_once()
            assert mock_lib.say.call_count == 1

    def test_perform1(self):
        mock_lib = MagicMock()
        with patch('performer.Performer', return_value=mock_lib):
            self.app.my_perform({
                "text": "my_text",
                "voice": True,
                "led": False,
            })
            assert mock_lib.say.called is True
            assert mock_lib.led_message.called is False

    def test_perform2(self):
        mock_lib = MagicMock()
        with patch('performer.Performer', return_value=mock_lib):
            self.app.my_perform({
                "text": "my_text",
                "voice": False,
                "led": True,
            })
            assert mock_lib.say.called is False
            assert mock_lib.led_message.called is True
