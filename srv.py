from flask import Flask, request, render_template, jsonify, make_response

import urllib.request
import urllib.parse
import subprocess
import time
import sys

import pprint
import os
import logging  # log
from logging.handlers import RotatingFileHandler  # log

SHOW_COMMAND = "bin/show_news"
show_direct_command = "bin/GO"

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return render_template('index.html', message="hoge")


@app.route('/ja')
def hello_world_ja():
    app.logger.info("hello world")
    return 'こんにちは 世界！'


@app.route('/image', methods=['POST'])
def get_image():
    app.logger.info("upload file")
    # https://qiita.com/5zm/items/ac8c9d1d74d012e682b4
    file = request.files['file']
    fileName = file.filename
    if fileName == "":
        make_response(jsonify({'result': 'filename must not empty.'}))

    UPLOAD_DIR = "/tmp"
    file.save(os.path.join(UPLOAD_DIR, "data.ppm"))

    res = subprocess.call(["sudo", "killall", "demo"])
    res = subprocess.call([show_direct_command,
                           os.path.join(UPLOAD_DIR, "data.ppm")])

    app.logger.info(res)

    return jsonify({"result": True})


@app.route('/news', methods=['POST'])
def get_news():
    if request.form["str"] != "":
        str = request.form["str"]

        app.logger.info(str)

        data = {"message": "えっ　なんだって？"}
        # ここでエンコードして文字 => バイトにする！
        data_encoded = urllib.parse.urlencode(data).encode("utf-8")
        with urllib.request.urlopen("http://192.168.207.42/voice/voice_data.php", data=data_encoded) as res:
            html = res.read().decode("utf-8")

            # run(>=3.5)
        res = subprocess.call(["sudo", "killall", "demo"])
        res = subprocess.call([SHOW_COMMAND, str])
        app.logger.info(res)

    return jsonify({"result": True})


@app.route('/reset')
def reset_news():
    res = subprocess.call(["sudo", "killall", "demo"])
    return "reset"


# 終了
# https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c

@app.route('/quit')
def quit():
    app.logger.info("QUIT..")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    sys.exit(0)
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

    app.run(host="0.0.0.0", port=5000)
    app.logger.info("start")
