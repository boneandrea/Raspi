# loopする
# - dequeue
# - parse data
# - call say
# - call LED

import sqlite3
import subprocess
import datetime


DBNAME = None
conn = None
CMD = "/home/pi/work/aquestalkpi/AquesTalkPi"
APLAY = "/usr/bin/aplay"


def init(dbname=None):
    global DBNAME, conn

    if DBNAME is None:
        DBNAME = dbname

    conn = sqlite3.connect(DBNAME)
    conn.row_factory = dict_factory
#    conn.row_factory = sqlite3.Row

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
        res = subprocess.run([CMD, "-s", str(speed), msg], stdout=subprocess.PIPE)
        wav = res.stdout
        p = subprocess.Popen([APLAY], stdin=subprocess.PIPE)
        p.communicate(wav)


def fuga():
    #    res = subprocess.call(["ls", "killall", "demo"])
    res = subprocess.call(["./a"])  # synchronized
    print(res)


def dequeue():

    c = conn.cursor()
    c.execute('select * from entries')
    entries = c.fetchall()
    for row in c.execute('select * from entries'):
        perform(row)

    return entries


def perform(dict_row):
    if True:
        say(dict_row)
    pass


def post_voice(voice_data):
    # ここでエンコードして文字 => バイトにする！
    voice_data_encoded = urllib.parse.urlencode(voice_data).encode("utf-8")
    with urllib.request.urlopen("http://192.168.207.42/voice/src/voice_data.php", data=voice_data_encoded) as res:
        html = res.read().decode("utf-8")


def enqueue(title, text):
    try:
        c = conn.cursor()
        stmt = "insert into entries (title, text, created) values (?,?,?)"
        c.execute(stmt, (title, text, datetime.datetime.now()))
        conn.commit()
        elem = c.execute('select * from entries where ROWID = last_insert_rowid()')
        return(elem.fetchone())

    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        raise e


if __name__ == '__main__':

    print(init("test.db"))
    fuga()
