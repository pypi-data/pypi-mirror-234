import json
from typing import Optional, Iterator
from typing import Any, List, Dict
from dwai.core.base_completions import BaseCompletions

class Completions(BaseCompletions):

    def run(self, prompt: str, message: List[Dict[str, Any]], stream: bool, **kwargs: Any):

        headers = dict()

        username, bot_name = "guest", "智能机器人"
        message.append({
            "sender_type": "USER",
            "sender_name": username,
            "text": prompt
        })

        data = {
            "bot_setting": [
                {
                    "bot_name": bot_name,
                    "content": "我是一个万能的机器人"
                }
            ],
            "messages": message,
            "reply_constraints": {
                "sender_type": "BOT",
                "sender_name": bot_name
            },
            **kwargs
        }

        resp = self.do_http(
            "/minimax/v1/text/chatcompletion_pro",
            headers,
            data,
            stream)

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
