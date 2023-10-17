import logging
from typing import Any, Optional, Dict, List

from dwai.unified.model_api.completions import UnifiedSDK
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.utils import get_from_dict_or_env
from pydantic.class_validators import root_validator

logger = logging.getLogger(__name__)


class DwUnifiedLLM(LLM):
    client: Any
    cloud: str = "alibaba"
    model: str = "qwen-plus-v1"
    api_key: str = "dw-BBAa68XBJUqiIj6xUQcC0KREnqmt5mPKQ52wkylD-Tw"
    api_base_china: str = "https://dwai.shizhuang-inc.com"
    api_base_singapore: str = "https://openai.shizhuang-inc.com"

    def __init__(self, cloud: str, model: str, api_key: str, api_base_china: str ="https://dwai.shizhuang-inc.com", api_base_singapore: str = "https://openai.shizhuang-inc.com", **kwargs: Any):
        super().__init__(**kwargs)
        self.cloud = cloud
        self.model = model
        self.api_key = api_key
        self.api_base_china = api_base_china
        self.api_base_singapore = api_base_singapore

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    @property
    def _llm_type(self) -> str:
        return "DwUnifiedLLM"

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        if values["client"] is not None:
            return values

        values["api_key"] = get_from_dict_or_env(
            values,
            "api_key",
            "API_KEY",
        )
        values["api_base_china"] = get_from_dict_or_env(
            values,
            "api_base_china",
            "API_BASE_CHINA",
        )
        values["api_base_singapore"] = get_from_dict_or_env(
            values,
            "api_base_singapore",
            "API_BASE_SINGAPORE",
        )

        try:
            import dwai
            from dwai.unified.model_api.completions import UnifiedSDK
            dwai.api_key = values["api_key"]
            dwai.api_base_china = values["api_base_china"]
            dwai.api_base_singapore = values["api_base_singapore"]
            values["client"] = UnifiedSDK()
        except ImportError:
            raise ModuleNotFoundError(
                "Could not import UnifiedSDK python package. "
                "Please install it with `pip3.10 install --no-cache-dir  dwai==0.2.1`."
            )
        return values

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        try:
            response = self.client.call(self.cloud, self.model, prompt=prompt)
            text = response.get("output", {}).get("text")
            if not response.get("Success"):
                raise RuntimeError(response.get("Message"))
        except Exception as e:
            raise RuntimeError(f"Error raised by broadscope service: {e}")
        if stop is not None:
            text = enforce_stop_tokens(text, stop)
        return text
