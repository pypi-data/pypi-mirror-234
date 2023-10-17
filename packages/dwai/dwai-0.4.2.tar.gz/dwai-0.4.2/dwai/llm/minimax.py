from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.utils import enforce_stop_tokens
from langchain.utils import get_from_dict_or_env
from pydantic.class_validators import root_validator

from typing import Any, Dict, List, Optional
from dwai.mini.completions import Completions

class MiniMaxLLM(LLM):
    client: Any
    api_key: str
    api_base: str
    history: Optional[List[Dict[str, Any]]] = []
    stream: bool = False
    parameters: Optional[Dict[str, Any]] = {}

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    @property
    def _llm_type(self) -> str:
        return "DwPanguLLM"

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:

        if values["client"] is not None:
            return values

        values["api_key"] = get_from_dict_or_env(
            values,
            "api_key",
            "DW_AI_KEY",
        )

        values["api_base"] = get_from_dict_or_env(
            values,
            "api_base",
            "DW_AI_BASE",
        )

        try:
            values["client"] = Completions(values["api_key"], values["api_base"])
        except AttributeError:
            raise ValueError(
                "`openai` has no `HW pangu SDK` attribute, this is likely "
                "due to an old version of the openai package. Try upgrading it "
                "with `pip3.10 install --no-cache-dir  dwai==0.2.1`."
            )

        return values

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> str:

        text = ""
        try:
            parameters = {
                "model": "abab5.5-chat",
                "tokens_to_generate": 1034,
                "temperature": 0.01,
                "top_p": 0.95
            } if not self.parameters else self.parameters
            messages = [] if not self.history else self.history
            response = self.client.run(prompt, messages, self.stream, **parameters)
            text = response.get("reply",  "")
        except Exception as e:
            raise RuntimeError(f"Error raised by ali bl service: {e}")

        if stop is not None:
            text = enforce_stop_tokens(text, stop)

        return text

