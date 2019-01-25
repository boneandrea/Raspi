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


def init(dbname=None):
    global DBNAME, conn

    if DBNAME is None:
        DBNAME = dbname

    conn = sqlite3.connect(DBNAME)
    conn.row_factory = sqlite3.Row

    return DBNAME


def fuga():
    #    res = subprocess.call(["ls", "killall", "demo"])
    res = subprocess.call(["./a"])  # synchronized
    print(res)


def dequeue():

    c = conn.cursor()
    c.execute('select * from entries')
    entries = c.fetchall()
    for row in c.execute('select * from entries'):
        print(row)

    stmt = "insert into entries (title, text, created) values (?,?,?)"
    c.execute(stmt, ("hoge", "fefefefef", datetime.datetime.now()))
    conn.commit()
    #    res = subprocess.call(["ls", "killall", "demo"])
    return entries


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
