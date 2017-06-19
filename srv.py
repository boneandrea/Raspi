# coding: utf-8

from flask import Flask, request

import urllib.request, urllib.parse
import subprocess
import time
import sys
import pprint

import os
import logging # log
from logging.handlers import RotatingFileHandler #log

show_command="/home/pi/bin/show_news"

app = Flask(__name__)
#app.debug=True

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ja')
def hello_world_ja():
    app.logger.info("hello world")
    return 'こんにちは 世界！'

@app.route('/news', methods=['POST'])
def get_news():
    pp = pprint.PrettyPrinter(indent=4)
    app.logger.info(pp)
    if request.form["str"] != "":
        str=request.form["str"]

        app.logger.info(str)

        data= {"message": "えっ　なんだって？"}
        # ここでエンコードして文字 => バイトにする！
        data_encoded = urllib.parse.urlencode(data).encode("utf-8")
        with urllib.request.urlopen("http://192.168.207.42/voice/voice_data.php", data=data_encoded) as res:
            html = res.read().decode("utf-8")
#            print(html)

          
            #run(>=3.5)
        res = subprocess.call(["sudo", "killall", "demo"])
        res = subprocess.call([show_command, str])
        app.logger.info(res)

    return 'set'

@app.route('/reset')
def reset_news():
    res = subprocess.call(["sudo", "killall", "demo"])
    return "reset"


# 終了
# https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c

@app.route('/quit')
def quit():
    app.logger.info("QUIT..抜けられない")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "quit"



def not_exist_makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == '__main__':

    debug_log = os.path.join(app.root_path, './logs/debug.log')
    not_exist_makedirs(os.path.dirname(debug_log))
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )
       
    debug_file_handler = RotatingFileHandler(
        debug_log, maxBytes=100000, backupCount=10
    )
    
    debug_file_handler.setLevel(logging.INFO)
    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)

    # handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1) # log
    # handler.setLevel(logging.DEBUG) # log
    # app.logger.addHandler(handler) # log

    app.run(host="192.168.207.42", port=5000)


