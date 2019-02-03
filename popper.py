# loopする
# - dequeue
# - parse data
# - call say
# - call LED
# 本番DBを設定して、ループ開始する(.envで判定？)


import sqlite3
import subprocess
import datetime
import draw_image
import time
import sys
import os
import logging  # log
import logging.config
import mock
import performer

# from logging.handlers import RotatingFileHandler  # log

logger = None


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Popper():

    conn = None
    DBNAME = None

    def init(self, dbname=None):
        if self.DBNAME is None:
            self.DBNAME = dbname

            self.conn = sqlite3.connect(self.DBNAME)
            self.conn.row_factory = dict_factory
            #    conn.row_factory = sqlite3.Row

        if logger != None:
            logger.info("init")

        return self.DBNAME

    def init_log(self):
        global logger
        logging.config.fileConfig('logging.conf')
        logger = logging.getLogger()

    def close(self):
        for h in logger.handlers:
            h.close()
            logger.removeHandler(h)
        self.conn.close()

    def dequeue(self):
        c = self.conn.cursor()
        c.execute('select * from entries')
        entries = c.fetchall()
        logger.info("{} records dequeued".format(len(entries)))
        for row in c.execute('select * from entries'):
            self.my_perform(row)
            c.execute('delete from entries where id=%s' % row["id"])
            self.conn.commit()

        return entries

    def enqueue(self, title, text, led=1, voice=1):
        try:
            c = self.conn.cursor()
            stmt = "insert into entries (title, text, led, voice, created) values (?,?,?,?,?)"
            c.execute(stmt, (title, text, led, voice, datetime.datetime.now()))
            self.conn.commit()
            elem = c.execute(
                'select * from entries where ROWID = last_insert_rowid()')
            return(elem.fetchone())

        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
            raise e

    def my_perform(self, dict_row):
        p=performer.Performer()

        if dict_row["led"] == True:
            p.led_message(dict_row)

        if dict_row["voice"] == True:
            p.say(dict_row)

        return True

    def mytrigger(self):
        mocked=mock.MyMock()
        mocked.hello()
        return self.dequeue()

    def main_loop(self):
        while True:
            self.dequeue()
            sys.stdout.flush()
            time.sleep(3)


if __name__ == '__main__':

    p = Popper()
    p.init_log()
    p.init("test.db")
    logging.info("start")

    text = "Hello"
    p.my_perform({
        "text": "start",
        "voice": True,
        "led": True
        })

#    p.conn.set_trace_callback(mytrigger)

    p.main_loop()
