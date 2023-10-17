import json
import threading
from typing import Any

import requests

import dwai

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
                model: str,
                stream: bool = False,
                temperature: float = 0.9
                ):

        headers = dict()
        headers["Content-Type"] = "application/json"
        headers["OpenAI-Organization"] = "Bearer %s" % dwai.api_key

        if stream:
            headers["Accept"] = "text/event-stream"

        data = {
            "frequency_penalty": 0,
            "max_tokens": 2000,
            "messages": [
                {
                    "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible. Include code language in markdown snippets whenever possible.",
                    "role": "system"
                },
                {
                    "content": prompt,
                    "role": "user"
                }
            ],
            "presence_penalty": 0.6,
            "stream": stream,
            "temperature": temperature
        }

        url = "%s%s%s%s" % (dwai.api_base_singapore, "/openai/deployments/", model, "/chat/completions")
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
