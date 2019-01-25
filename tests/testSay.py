import say
import unittest
import subprocess
import sys
import os


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
