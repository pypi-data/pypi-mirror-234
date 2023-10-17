import json
import threading
from typing import Any, List, Dict

import requests
import dwai

from dwai.bailian.model_api.exceptions import CompletionsRequestError

_thread_context = threading.local()

class BaseCompletions:
    """ 调用百联进行文本生成 """
    app_id = ""
    app_key = ""
    api_base = ""

    def __init__(self, app_id: str, app_key: str, api_base: str):
        self.app_id = app_id
        self.app_key = app_key
        self.api_base = api_base

    @classmethod
    def call(cls, *args, **kwargs) -> Any:
        raise NotImplementedError()

    def reqeust(self, app_id: str,
                prompt: str, history, stream, **kwargs):

        headers = dict()
        headers["Content-Type"] = "application/json;charset=UTF-8"
        headers["Authorization"] = "Bearer %s" % self.app_key
        headers["User-Agent "] = "dw"

        if stream:
            headers["Accept"] = "text/event-stream"

        self.validate(prompt=prompt)
        model = ""
        h = []
        if history is not None:
            for v in history:
                h.append(v.to_dict())

        data = {
            "model": model,
            "input": {
                "prompt": prompt,
                "history": h
            },
            "parameters": kwargs
        }

        url = "%s%s" % (dwai.api_base_china, "/bailian/services/aigc/text-generation/generation")
        session = self.__get_session()
        resp = session.request("POST",
                               url=url,
                               headers=headers,
                               data=json.dumps(data),
                               stream=stream)

        if not resp.ok:
            raise CompletionsRequestError("completion request error", resp.status_code, resp.text)

        return resp

    @staticmethod
    def __get_session() -> requests.Session:
        if not hasattr(_thread_context, "session"):
            _thread_context.session = requests.Session()

        return _thread_context.session

    def validate(self, prompt: str):


        if not self.api_base:
            raise ValueError("you need to get api base")

        if not self.app_key:
            raise ValueError("you need to set DW_API_KEY before calling api")

        if not self.app_id:
            raise ValueError("app id is required")

        if not prompt:
            raise ValueError("prompt is required")



