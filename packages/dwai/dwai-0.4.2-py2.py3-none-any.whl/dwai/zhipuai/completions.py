import json
from typing import Optional, Iterator
from typing import Any, List, Dict
from dwai.core.base_completions import BaseCompletions

class Completions(BaseCompletions):

    def run(self, prompt: str, message: List[Dict[str, Any]], stream: bool, **kwargs: Any):

        headers = dict()

        message.append({"role": "user", "content": prompt})
        model = "chatglm_std"
        if "model" in kwargs:
            model = kwargs.get("model")

        action = "invoke"
        if "action" in kwargs:
            action = kwargs.get("action")
            del kwargs["action"]

        data = {
            "prompt": message,
            **kwargs
        }

        url = "/zhipu/api/paas/v3/model-api/%s/%s" % (model, action)

        resp = self.do_http(url, headers, data, stream)

        if stream:
            return (json.loads(line) for line in self.parse_response_stream(resp.iter_lines()))
        else:
            return json.loads(resp.text)

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
