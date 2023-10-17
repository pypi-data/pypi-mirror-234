from typing import Iterator, Optional

import dwai

import posixpath
import json
from dwai.zhipuai.utils.http_client import get, post, stream
from dwai.zhipuai.utils.sse_client import SSEClient


class InvokeType:
    SYNC = "invoke"
    ASYNC = "async-invoke"
    SSE = "sse-invoke"


class ModelAPI:

    @classmethod
    def invoke(cls, **kwargs):
        url = cls._build_api_url(kwargs, InvokeType.SYNC)
        print("URL：", url)
        return post(url, kwargs)

    @classmethod
    def async_invoke(cls, **kwargs):
        url = cls._build_api_url(kwargs, InvokeType.ASYNC)
        return post(url, kwargs)

    @classmethod
    def query_async_invoke_result(cls, task_id: str):
        url = cls._build_api_url(None, InvokeType.ASYNC, task_id)
        return get(url, )

    @classmethod
    def sse_invoke(cls, **kwargs):
        url = cls._build_api_url(kwargs, InvokeType.SSE)
        data = stream(url, kwargs)
        # return SSEClient(data)
        return (line for line in cls.parse_response_stream(data.iter_lines()))

    @staticmethod
    def _build_api_url(kwargs, *path):
        if kwargs:
            if "model" not in kwargs:
                raise Exception("model param missed")
            model = kwargs.pop("model")
        else:
            model = "-"

        url = "%s%s" % (dwai.api_base_china, "/zhipu/api/paas/v3/model-api")
        return posixpath.join(url, model, *path)

    @classmethod
    def parse_response_stream(cls, resp: Iterator[bytes]) -> Iterator[str]:
        for line in resp:
            _line = cls.parse_stream_line(line)
            if _line is not None:
                yield {"data": _line}

    @staticmethod
    def parse_stream_line(line: bytes) -> Optional[str]:
        if line:
            if line.strip() == b"data:[DONE]":
                return None
            if line.startswith(b"data:"):
                line = line[len(b"data:"):]
                return line.decode("utf-8")
            else:
                return None
        return None
