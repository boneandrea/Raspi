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
# from logging.handlers import RotatingFileHandler  # log

CMD = "/home/pi/work/aquestalkpi/AquesTalkPi"
APLAY = "/usr/bin/aplay"
SHOW_COMMAND = "bin/show_news"
logger = None


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Perform():

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

    def say(row):
        speed = 100
        msg = row["text"]

        if msg is not None:
            res = subprocess.run([CMD, "-s", str(speed), msg],
                                 stdout=subprocess.PIPE)
            wav = res.stdout
            p = subprocess.Popen([APLAY], stdin=subprocess.PIPE)
            p.communicate(wav)

    def dequeue(self):
        c = self.conn.cursor()
        c.execute('select * from entries')
        entries = c.fetchall()
        logger.info("{} records dequeued".format(len(entries)))
        for row in c.execute('select * from entries'):
            self.my_perform(row)
            c.execute('delete from entries where id=%s' % row["id"])

        return entries

    def my_perform(self, dict_row):
        if False:
            led_message(dict_row)

        if False:
            say(dict_row)

        return True

    def led_message(self, row):
        try:
            if self.draw(row["text"]):
                print("fe")
                # run demo if success
                res = subprocess.run([SHOW_COMMAND, row["text"]])
                return True
            else:
                return False

        except KeyError as e:
            raise

    def enqueue(self, title, text):
        try:
            c = self.conn.cursor()
            stmt = "insert into entries (title, text, created) values (?,?,?)"
            c.execute(stmt, (title, text, datetime.datetime.now()))
            self.conn.commit()
            elem = c.execute(
                'select * from entries where ROWID = last_insert_rowid()')
            return(elem.fetchone())

        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
            raise e

    def draw(self, message):
        try:
            res = subprocess.run(["sudo", "killall", "demo"])
            draw_image.create([{
                "char": message,
                "size": "full",
                "color": "#55aaff",
                "background": "#004411"
            }],
                outputFile="bin/img/news",
                height=32
            )
            return True
        except Exception as e:
            print(e)
            raise e

        return False

    def mytrigger(self):
        return self.dequeue()

    def main_loop(self):
        while True:
            self.dequeue()
            print(".", end="")
            sys.stdout.flush()
            time.sleep(3)


if __name__ == '__main__':

    p = Perform()
    p.init_log()
    p.init("test.db")
    logging.info("start")

    text = "Hello"
    p.my_perform({"text": text})

#    p.conn.set_trace_callback(mytrigger)

    p.main_loop()
