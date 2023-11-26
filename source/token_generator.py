import json
from threading import Thread
from time import sleep
import os

def token():
    while True:
        token = os.popen('/usr/bin/bash source/token.sh').read()[49:85]
        print('Token generator result:', token)
        with open('source/token.json', 'w') as f:
            json.dump(token, f)
        sleep(1800)

def main():
    thread = Thread(target = token)
    thread.start()