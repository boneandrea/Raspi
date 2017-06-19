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

show_command="show_news"

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ja')
def hello_world_ja():
    return 'こんにちは 世界！'

@app.route('/news', methods=['POST'])
def get_news():
    pp = pprint.PrettyPrinter(indent=4)
    if request.form["str"] != "":
        str=request.form["str"]

        #Hl: "/voice/voice_data.php",
        data= {"message": "えっ　なんだって？"}
        # ここでエンコードして文字→バイトにする！
        data_encoded = urllib.parse.urlencode(data).encode("utf-8")
        with urllib.request.urlopen("http://192.168.207.42/voice/voice_data.php", data=data_encoded) as res:
            html = res.read().decode("utf-8")
#            print(html)

          
            #run(>=3.5)
        res = subprocess.call(["sudo", "killall", "demo"])
        res = subprocess.call([show_command, str])
        print (res)
	
#    pp.pprint( "body: {0}".format(request.data ))
    return 'set'

@app.route('/reset')
def reset_news():
    res = subprocess.call(["sudo", "killall", "demo"])
    return "reset"


@app.route('/quit')
def quit():
    app.logger.info("QUIT..抜けられない")
    return "quit"
#    app.terminate()


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
#    debug_file_handler.setFormatter(formatter)
    app.logger.addHandler(debug_file_handler)


    # handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1) # log
    # handler.setLevel(logging.DEBUG) # log
    # app.logger.addHandler(handler) # log

    app.run(host="192.168.207.42", port=5000)


