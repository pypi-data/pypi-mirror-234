from dwai.llm.bl import AliBlLLM
from dwai.llm.tx import TiOneLLM
from dwai.llm.pangu import HwPanguLLM
from dwai.llm.minimax import MiniMaxLLM
from dwai.llm.azure import AzureChatOpenAI
from dwai.llm.zhipu import ZhiPuLLM

DW_LLM_MAP = {
    "ali.qwen": AliBlLLM,
    "hw.pangu": HwPanguLLM,
    "ti.one": TiOneLLM,
    "mini.max": MiniMaxLLM,
    "zhipu.ai": ZhiPuLLM,
    "azure": AzureChatOpenAI
}

default_api_key = "dw-BBAa68XBJUqiIj6xUQcC0KREnqmt5mPKQ52wkylD-Tw"
default_api_base = "https://dwai.shizhuang-inc.com"

class DwlLm(object):
    """获取模型参数"""

    def __call__(self, model: str, api_key: str = default_api_key, api_base: str = default_api_base, stream: bool = False, **kwargs):

        if model not in DW_LLM_MAP.keys():
            raise RuntimeError("NOT FOUND DW LLM MODEL")

        llm_model = DW_LLM_MAP.get(model)
        parameters = kwargs if kwargs else {}

        if model == "azure":
            return llm_model(
                deployment_name=kwargs.get("deployment_name"),
                temperature=kwargs.get("temperature"),
                openai_api_version=kwargs.get("openai_api_version"),
                openai_api_key=api_key,
                openai_api_base=api_base,
                openai_api_type=kwargs.get("openai_api_type"),
                openai_organization=kwargs.get("openai_organization"),
                streaming=stream
            )

        return llm_model(
            api_key=api_key,
            api_base=api_base,
            stream=stream,
            parameters=parameters,
        )


def load_dw_llm(model: str, api_key: str = default_api_key, api_base: str = default_api_base, stream: bool = False, **kwargs):

    if model not in DW_LLM_MAP.keys():
        raise RuntimeError("NOT FOUND DW LLM MODEL")

    llm_model = DW_LLM_MAP.get(model)
    parameters = kwargs if kwargs else {}

    if model == "azure":
        return llm_model(
            deployment_name=kwargs.get("deployment_name"),
            temperature=kwargs.get("temperature"),
            openai_api_version=kwargs.get("openai_api_version"),
            openai_api_key=api_key,
            openai_api_base=api_base,
            openai_api_type=kwargs.get("openai_api_type"),
            openai_organization=kwargs.get("openai_organization"),
            streaming=stream
        )

    return llm_model(
        api_key=api_key,
        api_base=api_base,
        stream=stream,
        parameters=parameters,
    )
