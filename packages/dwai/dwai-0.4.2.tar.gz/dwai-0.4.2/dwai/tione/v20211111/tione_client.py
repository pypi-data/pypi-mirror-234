# -*- coding: utf8 -*-

import json
from typing import Iterator, Optional

from dwai.tione.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from dwai.tione.common.base_completions import BaseCompletions
from dwai.tione.v20211111 import models

class TioneClient(BaseCompletions):
    _apiVersion = '2021-11-11'
    _endpoint = 'tione.tencentcloudapi.com'
    _service = 'tione'

    def call(self,
             action: str = None,
             max_tokens: str = None,
             content: str = None,
             top_p: float = 0.0,
             stream: bool = False):
        resp = self.reqeust(
            action=action,
            max_tokens=max_tokens,
            content=content,
            top_p=top_p,
            stream=stream,
        )

        if stream:
            return (json.loads(line) for line in self.parse_response_stream(resp.iter_lines()))
        else:
            return json.loads(resp.text)

    def ChatCompletion(self, model: str, content, stream=False, top_p=None, max_tokens=None):
        try:
            response = self.call(
                "ChatCompletion",
                content=content,
                stream=stream,
                top_p=top_p,
                max_tokens=max_tokens
            )
            model = models.ChatCompletionResponse()
            model._deserialize(response)
            return model
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(type(e).__name__, str(e))

    def parse_response_stream(self, resp: Iterator[bytes]) -> Iterator[str]:
        for line in resp:
            _line = self.parse_stream_line(line)
            if _line is not None:
                yield _line

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
