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

DBNAME = None
conn = None
CMD = "/home/pi/work/aquestalkpi/AquesTalkPi"
APLAY = "/usr/bin/aplay"
SHOW_COMMAND = "bin/show_news"
logger = None


def init(dbname=None):
    global DBNAME, conn

    if DBNAME is None:
        DBNAME = dbname

    conn = sqlite3.connect(DBNAME)
    conn.row_factory = dict_factory
#    conn.row_factory = sqlite3.Row

    logger.info("init")
    return DBNAME


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def say(row):
    speed = 100
    msg = row["text"]

    if msg is not None:
        print("RUN")
        print([CMD, "-s", str(speed), msg])
        res = subprocess.run([CMD, "-s", str(speed), msg],
                             stdout=subprocess.PIPE)
        wav = res.stdout
        p = subprocess.Popen([APLAY], stdin=subprocess.PIPE)
        p.communicate(wav)


def dequeue():

    c = conn.cursor()
    c.execute('select * from entries')
    entries = c.fetchall()
    for row in c.execute('select * from entries'):
        perform(row)

    logger.info("{} records dequeued".format(len(entries)))
    return entries


def perform(dict_row):
    if True:
        led_message(dict_row)

    if True:
        say(dict_row)


def led_message(row):
    try:
        if draw(row["text"]):
            # run demo if success
            res = subprocess.run([SHOW_COMMAND, row["text"]])
            print(res)
            return True
        else:
            return False

    except KeyError as e:
        raise


def enqueue(title, text):
    try:
        c = conn.cursor()
        stmt = "insert into entries (title, text, created) values (?,?,?)"
        c.execute(stmt, (title, text, datetime.datetime.now()))
        conn.commit()
        elem = c.execute(
            'select * from entries where ROWID = last_insert_rowid()')
        return(elem.fetchone())

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        raise e


def draw(message):
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
        raise e
        return False

        pass


def mytrigger():
    print("trigger")
    pass


def init_log():
    global logger
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()


if __name__ == '__main__':

    init_log()
    init("test.db")
    logging.info("start")

    text = "Hello"
    perform({"text": text})

    conn.set_trace_callback(mytrigger)

    while True:
        dequeue()
        time.sleep(3)
