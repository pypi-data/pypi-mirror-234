import json
import threading
from typing import Any, List, Dict
from abc import ABC, abstractmethod
import requests
from dwai.core.exceptions import CompletionsRequestError

_thread_context = threading.local()

class BaseCompletions(ABC):
    """ 对话API基类 """
    api_key = ""
    api_base = ""

    def __init__(self, api_key: str, api_base: str):
        self.api_key = api_key
        self.api_base = api_base

    @classmethod
    def call(cls, *args, **kwargs) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def run(self, prompt: str, history: List[Dict[str, Any]], stream: bool, **kwargs: Any):
        pass

    def do_http(self, api_path, headers, data, stream):

        headers["Content-Type"] = "application/json;charset=UTF-8"
        headers["Authorization"] = "Bearer %s" % self.api_key
        headers["User-Agent "] = "dw"

        url = "%s%s" % (self.api_base, api_path)

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




