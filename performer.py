import subprocess
import datetime
import draw_image
import time
import sys
import os
import logging  # log
import logging.config
import mock

CMD = "/home/pi/work/aquestalkpi/AquesTalkPi"
APLAY = "/usr/bin/aplay"
SHOW_COMMAND = "bin/show_news"

class Performer:
    def led_message(self, row):
        try:
            if self.draw(row["text"]):
                # run demo if success
                res = subprocess.run(["sudo", "killall", "demo"])
                res = subprocess.run([SHOW_COMMAND, row["text"]])
                return True
            else:
                return False

        except KeyError as e:
            raise

    def say(self,row):
        speed = 100
        msg = row["text"]
        try:
            if msg:
                res = subprocess.run([CMD, "-s", str(speed), msg],
                                 stdout=subprocess.PIPE)
                wav = res.stdout
                p = subprocess.Popen([APLAY], stdin=subprocess.PIPE)
                p.communicate(wav)
                return True
            else:
                return False

        except KeyError as e:
            raise

    def draw(self, message):
        try:
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
