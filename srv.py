# coding: utf-8

from flask import Flask, request

import urllib.request, urllib.parse
import subprocess
import pprint

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
        res = subprocess.call(["NEWS", str])
        print (res)
	
#    pp.pprint( "body: {0}".format(request.data ))
    return 'set'

@app.route('/reset')
def reset_news():
    res = subprocess.call(["sudo", "killall", "demo"])
    return "reset"


if __name__ == '__main__':
    app.run(host="192.168.207.42", port=5000)


