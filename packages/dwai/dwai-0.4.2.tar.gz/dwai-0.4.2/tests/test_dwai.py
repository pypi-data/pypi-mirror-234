#!/usr/bin/env python

"""Tests for `dwai` package."""
import unittest
from datetime import datetime

from dwai.pangu.model_api.completions import PanGuCompletions
from dwai.tione.completions import TiOneCompletions
from dwai.bailian.model_api.completions import Completions
from dwai.mini.completions import Completions as MinimaxCompletions
from dwai.pangu.model_api.message import Message

from dwai.zhipuai.model_api.api import ModelAPI
API_KEY = "dw-BBAa68XBJUqiIj6xUQcC0KREnqmt5mPKQ52wkylD-Tw"
API_BASE = "https://dwai.shizhuang-inc.com"

import dwai

dwai.api_key = "dw-BBAa68XBJUqiIj6xUQcC0KREnqmt5mPKQ52wkylD-Tw"
dwai.api_base = "https://dwai.shizhuang-inc.com"

class TestDwai(unittest.TestCase):
    """Tests for `dwai` package."""

    def test_bailian_qa(self):
        """Test something."""

        chat = Completions(API_KEY, API_BASE)
        params = {
                "top_p": 0.3,
                "has_thoughts": True
            }

        resp = chat.run_v1("""你是一个智能文档助手，使用以下上下文来回答用户的问题,如果你不知道答案，就说你不知道，不要试图编造答案。
问题: 1+1=?
有用的答案:""", [], False, **params)
        print(resp)

    def test_bailian_qa_stream(self):
        chat = Completions(API_KEY, API_BASE)
        resp = chat.call(
            app_id="1e4ddc3659324ad0b8a0039230f1dba3",
            prompt="你好",
            stream=True)
        for line in resp:
            now = datetime.now()
            print("%s: %s" % (now, line), end="\n", flush=True)

    def test_minimax_qa(self):
        chat = Completions(API_KEY, API_BASE)
    def test_zhipuai_invoke(self):
        model = ModelAPI()
        resp = model.invoke(
            model="chatglm_std",
            prompt=[{"role": "user", "content": "人工智能"}],
            top_p=0.7,
            temperature=0.9,
        )
        print(resp)

    def test_zhipuai_sse_invoke(self):
        model = ModelAPI()
        resp = model.sse_invoke(
            model="chatglm_std",
            prompt=[{"role": "user", "content": "人工智能"}],
            top_p=0.7,
            temperature=0.9,
        )
        print("d.", resp)
        for line in resp:
            now = datetime.now()
            print("%s: %s" % (now, line), end="\n", flush=True)

    def test_zhipuai_async_invoke(self):
        model = ModelAPI
        response = model.async_invoke(
            model="chatglm_std",
            prompt=[{"role": "user", "content": "人工智能"}],
            top_p=0.7,
            temperature=0.9,
        )
        print(response)

    def test_pangu(self):
        """Test something."""
        chat = PanGuCompletions(API_KEY, API_BASE)
        params = dict(max_tokens=600, temperature=0.9)
        messages = [
            Message("system", "请用幼儿园老师的口吻回答问题，注意语气温和亲切，通过提问、引导、赞美等方式，激发学生的思维和想象力。").to_dict(),
            Message("user", "写一首诗").to_dict()
        ]
        resp = chat.run(
            prompt="",
            messages=messages,
            stream=False,
            **params
        )
        print(resp)

    def test_pangu_stream(self):
        """Test something."""
        chat = PanGuCompletions(API_KEY, API_BASE)
        params = dict(max_tokens=600, temperature=0.9,)
        messages = [
            Message("system", "请用幼儿园老师的口吻回答问题，注意语气温和亲切，通过提问、引导、赞美等方式，激发学生的思维和想象力。"),
            Message("user", "写一首诗")
        ]
        resp = chat.run(
            prompt="",
            messages=messages,
            stream=True,
            **params
        )
        # print(resp)
        for line in resp:
            now = datetime.now()
            print("%s: %s" % (now, line), end="\n", flush=True)

    def test_tione(self):
        """Test something."""
        chat = TiOneCompletions(API_KEY, API_BASE)
        params = dict(max_tokens=600, top_p=0.3, )
        resp = chat.run("2+2=?", [], False, **params)
        print(resp)

    def test_minimax(self):
        """Test something."""
        chat = MinimaxCompletions(API_KEY, API_BASE)
        params = {
            "model": "abab5.5-chat",
            "tokens_to_generate": 1034,
            "temperature": 0.01,
            "top_p": 0.95
        }
        resp = chat.run("2+2=?", [], False, **params)
        print(resp)

    def test_unified(self):
        from dwai.unified.dw import UnifiedSDK

        # 所有模型自定义参数都放到各自的params中，会自动传入接口Body
        # 阿里千问
        qw_sdk = UnifiedSDK("ali.qwen", API_KEY, API_BASE)
        params = {
            "top_p": 0.3,
            "has_thoughts": True
        }
        print("ali.qs:", qw_sdk("1+1=?", [], False, **params))

        # 华为pangu
        hw_sdk = UnifiedSDK("hw.pangu", API_KEY, API_BASE)
        params = dict(max_tokens=600, temperature=0.9)
        messages = [
            Message("system",
                    "请用幼儿园老师的口吻回答问题，注意语气温和亲切，通过提问、引导、赞美等方式，激发学生的思维和想象力。").to_dict(),
            Message("user", "写一首诗").to_dict()
        ]
        print("hw.qs:", hw_sdk("1+1=?", messages, False, **params))

        # mini Max
        mini_sdk = UnifiedSDK("minimax", API_KEY, API_BASE)
        params = {
            "model": "abab5.5-chat",
            "tokens_to_generate": 1034,
            "temperature": 0.01,
            "top_p": 0.95
        }
        print("mini.qs:", mini_sdk("1+1=?", [], False, **params))

        # 腾讯
        params = dict(max_tokens=600, top_p=0.3, )
        ti_sdk = UnifiedSDK("ti.one", API_KEY, API_BASE)
        print("ti.sdk:", ti_sdk("2+2=?", [], False, **params))

        # 金山智普
        zhipu_sdk = UnifiedSDK("zhipu", API_KEY, API_BASE)
        params = dict(top_p=0.7, temperature=0.9)
        print("zhipu.qs:", zhipu_sdk("你的参数量大概是多少？", [], False, **params))

        # 火山方舟
        fz_sdk = UnifiedSDK("fang.zhou", API_KEY, API_BASE)
        params = dict(temperature=0.9)
        print("ff.qs:", fz_sdk("1+1=？", [], False, **params))

