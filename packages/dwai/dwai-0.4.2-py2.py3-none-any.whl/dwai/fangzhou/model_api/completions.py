import json
from typing import Optional, Iterator, List, Any, Dict

from dwai.core.base_completions import BaseCompletions

class Completions(BaseCompletions):

    def run(self, prompt: str, message: List[Dict[str, Any]], stream: bool, **kwargs: Any):

        headers = dict()
        if stream:
            headers["Accept"] = "text/event-stream"

        self.validate(prompt=prompt)

        message.append({
            "role": "user",
            "content": prompt
        })

        data = {
            "messages": message,
            **kwargs
        }

        resp = self.do_http(
            "/fangzhou/chat/completion",
            headers,
            data,
            stream)

        if stream:
            return (line for line in self.parse_response_stream(resp.iter_lines()))
        else:
            return resp.text

    def validate(self, prompt: str):

        if not self.api_base:
            raise ValueError("you need to get api base")

        if not self.api_key:
            raise ValueError("you need to set DW_API_KEY before calling api")

        if not prompt:
            raise ValueError("prompt is required")

    def parse_response_stream(self, resp: Iterator[bytes]) -> Iterator[str]:
        for line in resp:
            _line = self.parse_stream_line(line)
            if _line is not None:
                yield _line

    @staticmethod
    def parse_stream_line(line: bytes) -> Optional[str]:
        if line:
            if line.strip() == b"data: [DONE]":
                return None
            if line.startswith(b"data: "):
                line = line[len(b"data: "):]
                return line.decode("utf-8")
            else:
                return None
        return None
