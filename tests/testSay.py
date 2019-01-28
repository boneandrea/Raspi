import say
import unittest
import subprocess
import sys
import os
from unittest.mock import patch, MagicMock, call


DB_PROGRAM = "sqlite3"
DB_SCHEMA = "schema.sql"
TEST_DB = "test.db"


class TestSay(unittest.TestCase):

    def initDb(self):
        p = subprocess.Popen([DB_PROGRAM, TEST_DB], stdin=subprocess.PIPE)
        with open(DB_SCHEMA, "r") as f:
            data = f.read()
            p.communicate(data.encode())

    def setUp(self):
        self.initDb()
        self.app = say.init(TEST_DB)

    def tearDown(self):
        pass

    def test_dequeue(self):
        data = say.dequeue()
        self.assertEqual(0, len(data))

    def test_enqueue(self):
        data = say.enqueue(title="TITLE", text="テキスト")
        self.assertEqual("テキスト", data["text"])
        self.assertIsNotNone(data)
        say.dequeue()

    # def test_1action(self):
    #     mock_lib = MagicMock()
    #     with patch('say', return_value=mock_lib):
    #         say.enqueue()
    #         say.enqueue(title="TITLE", text="テキスト")

    #     assert mock_lib.perfome.called is True

    #     assert True is True
#        assert mock_lib.enqueue.called is True
        # say.enqueue(title="TITLE", text="テキスト")
        # say.dequeue()
        # self.assertIsNotNone(data)
