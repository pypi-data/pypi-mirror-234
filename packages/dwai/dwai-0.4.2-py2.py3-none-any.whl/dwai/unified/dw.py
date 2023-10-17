from dwai.bailian.model_api.completions import Completions as AliBlCompletions
from dwai.pangu.model_api.completions import PanGuCompletions as HwPgCompletions
from dwai.tione.completions import TiOneCompletions
from dwai.mini.completions import Completions as MiniCompletions
from dwai.core.base_completions import BaseCompletions
from dwai.zhipuai.completions import Completions as ZhipuCompletions
from dwai.fangzhou.model_api.completions import Completions as FzCompletions
from typing import Any, List, Dict, Optional

DW_AI_MAP = {
    "ali.qwen": AliBlCompletions,
    "hw.pangu": HwPgCompletions,
    "ti.one": TiOneCompletions,
    "minimax": MiniCompletions,
    "zhipu": ZhipuCompletions,
    "fang.zhou": FzCompletions
}

class UnifiedSDK(object):

    client: Optional[BaseCompletions]

    def __init__(self, cloud: str, api_key: str, api_base: str):
        if cloud not in DW_AI_MAP.keys():
            raise RuntimeError("NOT FOUND DW LLM MODEL")

        self.client = DW_AI_MAP.get(cloud)(api_key, api_base)

    def __call__(self, prompt: str, message: List[Dict[str, Any]], stream: bool, **kwargs: Any):
        return self.client.run(prompt, message, stream, **kwargs)
