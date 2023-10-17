# -*- coding:utf-8 -*-
import json
import logging

import requests
from typing import Dict, Optional, Iterator

import dwai


def post(api_url, params):
    try:
        headers = dict()
        headers["Content-Type"] = "application/json;charset=UTF-8"
        headers["Authorization"] = dwai.api_key

        resp = requests.post(
            url=api_url, data=json.dumps(params), headers=headers, timeout=dwai.api_timeout_seconds
        )
        if requests.codes.ok != resp.status_code:
            raise Exception("响应异常：" + resp.content)
        return json.loads(resp.text)
    except Exception as e:
        logging.exception("请求异常", e)


def stream(api_url, params):
    try:
        headers = dict()
        headers["Authorization"] = dwai.api_key

        resp = requests.post(
            api_url,
            stream=True,
            headers=headers,
            json=params,
            timeout=dwai.api_timeout_seconds,
        )
        if requests.codes.ok != resp.status_code:
            raise Exception("请求异常")
        return resp
    except Exception as e:
        logging.exception("请求异常", e)


def get(api_url):
    try:
        headers = dict()
        headers["Authorization"] = dwai.api_key
        resp = requests.get(api_url, headers=headers, timeout=dwai.api_timeout_seconds)
        if requests.codes.ok != resp.status_code:
            raise Exception("响应异常：" + resp.content)
        return json.loads(resp.text)
    except Exception as e:
        logging.exception("请求异常", e)
