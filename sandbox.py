#!/usr/bin/python3
import sys
import time
import requests
import urllib.parse

rovIP = "localhost"

# print to stderr to avoid SDL messages
def prerr(msg):
    wrerr(msg + "\r\n")

# write to stderr.  pygame clutters up stdout because of a bug
def wrerr(msg): 
    sys.stderr.write(msg)

while True:
    values = [100, 200, 50]

    # map joystick axis values to servos
    my_query = {
            0: "500",
            1: "200",
            4: "600"
            }

    my_query = urllib.parse.urlencode(my_query)

    prerr("about to send: " + my_query)
    try:
        r = requests.get("http://" + rovIP + ":5000" + "/?" + my_query)
        prerr("sent")
        prerr(r.text)
    except Exception as e:
        prerr(str(e))
    time.sleep(0.2) 
