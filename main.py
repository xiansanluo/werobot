#!/usr/bin/python
#coding:utf-8
import werobot
import os
import re
import requests
import threading
import time
import logging
import json
# import multiprocessing
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TOKEN = os.environ.get('WE_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
ACCESS_TOKEN = ''
SCENE_ID = os.environ.get('SCENE_ID')

robot = werobot.WeRoBot(token=TOKEN)
# robot.config["APP_ID"] = "Your AppID"
# robot.config['ENCODING_AES_KEY'] = 'Your Encoding AES Key'

def get_token():
    global ACCESS_TOKEN
    payload = {'grant_type': 'client_credentials',
               'client_id': CLIENT_ID,
               'client_secret': CLIENT_SECRET
               }
    while True:
        r = requests.post('https://aip.baidubce.com/oauth/2.0/token', data=payload)
        if r.status_code == requests.codes.ok:
            ACCESS_TOKEN = r.json()["access_token"]
            print threading.current_thread().name, "update new access token:", ACCESS_TOKEN
            time.sleep(3600 * 24 * 25)

@robot.text
def handle(message):
    global ACCESS_TOKEN
    payload = {'scene_id': SCENE_ID,
                'query': message.content,
                'session_id': message.source
               }
    headers = {"Content-Type": "application/json"}
    url = 'https://aip.baidubce.com/rpc/2.0/solution/v1/unit_utterance'
    r = requests.post(url + '?access_token=' + ACCESS_TOKEN, json=payload, headers=headers)
    for l in r.json()["result"]["action_list"]:
        return l["say"]

# @robot.text
# def b():
#     if re.compile(".*?bb.*?").match(message.content):
#         return "正文中含有 b "
#
# @robot.text
# def c():
#     if re.compile(".*?c.*?").match(message.content) or message.content == "d":
#         return "正文中含有 c 或正文为 d"

def run():
    robot.config['HOST'] = '0.0.0.0'
    robot.config['PORT'] = 8080
    robot.run()
# if __name__ == '__main__':
#     p = multiprocessing.Process(target=get_token, args=())
#     p.start()
#     run()
if __name__ == '__main__':
    t = threading.Thread(target=get_token, args=())
    t.start()
    run()