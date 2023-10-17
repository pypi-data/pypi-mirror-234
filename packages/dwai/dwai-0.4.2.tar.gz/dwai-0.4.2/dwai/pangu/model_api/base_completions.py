import json
import threading
import uuid
from typing import Dict, Any, List

import requests

import dwai
from dwai.pangu.model_api.message import Message
_thread_context = threading.local()


class CompletionsRequestError(Exception):
    def __init__(self,
                 message=None,
                 status_code=None,
                 response_body=None
                 ):
        super(CompletionsRequestError, self).__init__(message)

        self.message = message
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self):
        return "%s: status_code=%s, response_body=%s" % (
            self.message,
            self.status_code,
            self.response_body
        )

    def __repr__(self):
        return "(message=%r, status_code=%r, response_body=%r)" % (
            self.message,
            self.status_code,
            self.response_body
        )


class BaseCompletions:

    @classmethod
    def call(cls, *args, **kwargs) -> Any:
        raise NotImplementedError()

    def reqeust(self,
                prompt: str,
                max_tokens: str = None,
                messages: List[Message] = None,
                temperature: float = 0.0,
                model: str = None,
                stream: bool = False):

        headers = dict()
        headers["Content-Type"] = "application/json;charset=UTF-8"
        headers["Authorization"] = "Bearer %s" % dwai.api_key

        data = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "Prompt": prompt,
            "stream": stream
        }

        url = "%s%s" % (dwai.api_base_china, "/pangu/v1/chat/completions")
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




