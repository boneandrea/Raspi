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
        self.conn=self._initDb()
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

    #################### </helper>

    def test_init(self):
        assert self.conn is not None

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

    def test_mytrigger(self):
        self.assertTrue(type(self.app.mytrigger()) is list)

    def test_mock_action(self):
        mock_lib = MagicMock()
        with patch('mock.MyMock', return_value=mock_lib):
            self.app.mytrigger()
            assert mock_lib.hello.called is True

    def test_perform(self):
        mock_lib = MagicMock()
        with patch('performer.Performer', return_value=mock_lib):
            self.app.my_perform({
                "text": "my_text",
                "voice": True,
                "led": True
                })
            assert mock_lib.led_message.called is True
            assert mock_lib.say.called is True


            # perform.enqueue(title="TITLE", text="テキスト")

    #     assert True is True
#        assert mock_lib.enqueue.called is True
        # perform.enqueue(title="TITLE", text="テキスト")
        # perform.dequeue()
        # self.assertIsNotNone(data)
