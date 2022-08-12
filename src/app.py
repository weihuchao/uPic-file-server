#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 23:42
# @Author  : Huchao Wei
import base64
import datetime
import json
import os.path

from flask import Flask
from flask import request

app = Flask(__name__, static_url_path='/static')
FLASK_HOST = os.environ['FLASK_HOST']
PUSH_SECRET = os.environ['PUSH_SECRET']


def get_now_str():
    return datetime.datetime.now().strftime('%H%M%S')


def get_img_dir():
    today = datetime.datetime.now().strftime('%Y%m%d')
    img_dir = os.path.join('static', 'img', today)
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    return img_dir


@app.route("/push/", methods=["POST"])
def post_install():
    content = request.get_json()
    if content['secret'] != PUSH_SECRET:
        return ''
    file_path = '{}/{}-{}.{}'.format(get_img_dir(), content['filename'], get_now_str(), content['suffix'])
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(content['file']))
    return json.dumps({"data": '{}{}'.format(FLASK_HOST, file_path)})
