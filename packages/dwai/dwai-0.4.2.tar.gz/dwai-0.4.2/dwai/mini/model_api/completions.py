import json
from typing import Dict, Optional, Iterator, List

from dwai.mini.model_api.base_completions import BaseCompletions


class MiniCompletions(BaseCompletions):
    def call(self,
             prompt: str,
             model: str,
             temperature: float,
             stream: bool = False):
        resp = self.reqeust(prompt=prompt,
                            stream=stream,
                            model=model,
                            temperature=temperature)

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
