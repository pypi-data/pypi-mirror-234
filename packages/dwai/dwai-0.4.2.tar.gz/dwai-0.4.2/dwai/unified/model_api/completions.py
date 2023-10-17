import json
import dwai
from jsonpath_ng import parse
from dwai.azure.model_api.completions import AzureCompletions
from dwai.bailian.model_api.completions import Completions
from dwai.mini.model_api.completions import MiniCompletions
from dwai.pangu.model_api.completions import PanGuCompletions
from dwai.tione.v20211111.tione_client import TioneClient
from dwai.zhipuai.model_api.api import ModelAPI


def azure_qa(**kwargs):
    chat = AzureCompletions()
    json_output = chat.call(prompt=kwargs.get('prompt'), model=kwargs.get('model'), temperature=kwargs.get('temperature'), stream=False)
    matches = parse('$.choices[0].message.content').find(json_output)
    if len(matches) > 0:
        return {"output": {"text": matches[0].value}, "Success": True}
    else:
        return {}


def mini_qa(**kwargs):
    chat = MiniCompletions()
    json_output = chat.call(prompt=kwargs.get('prompt'), model=kwargs.get('model'), temperature=kwargs.get('temperature'), stream=False)
    matches = parse('$.choices[0].messages[0].text').find(json_output)
    if len(matches) > 0:
        return {"output": {"text": matches[0].value}, "Success": True}
    else:
        return {}


def dwai_bailian_qa(**kwargs):
    chat = Completions()
    json_output = chat.call(app_id="1e4ddc3659324ad0b8a0039230f1dba3", prompt=kwargs.get('prompt'),
                            model=kwargs.get('model'))
    matches = parse('$.output.text').find(json_output)
    if len(matches) > 0:
        return {"output": {"text": matches[0].value}, "Success": True}
    else:
        return {}


def zhipuai_chatglm_std(**kwargs):
    model = ModelAPI()
    json_output = model.invoke(model=kwargs.get('model'), prompt=[{"role": "user", "content": kwargs.get('prompt')}],
                               top_p=kwargs.get('top_p', 0.7), temperature=kwargs.get('temperature', 0.9))
    matches = parse('$.data.choices[0].content').find(json_output)
    if len(matches) > 0:
        return {"output": {"text": matches[0].value}, "Success": True}
    else:
        return {}


def pangu_completions(**kwargs):
    chat = PanGuCompletions()
    json_output = chat.call(max_tokens=kwargs.get('max_tokens', 600), prompt="",
                            messages=[{"role": "user", "content": kwargs.get('prompt')}],
                            temperature=kwargs.get('temperature', 0.9), model=kwargs.get('model'))
    matches = parse('$.choices[0].message.content').find(json_output)
    if len(matches) > 0:
        return {"output": {"text": matches[0].value}, "Success": True}
    else:
        return {}


def tione_chat_completion(**kwargs):
    chat = TioneClient()
    content = chat.ChatCompletion(content=kwargs.get('prompt'), model=kwargs.get('model')).to_json_string()
    json_obj = json.loads(content)
    matches = parse('$.Choices[0].Message.Content').find(json_obj)
    if len(matches) > 0:
        return {"output": {"text": matches[0].value}, "Success": True}
    else:
        return {}


class UnifiedSDK:
    def __init__(self):

        dwai.api_base_china = "https://dwai.shizhuang-inc.com"
        dwai.api_base_singapore = "https://openai.shizhuang-inc.com"

        self.route_map = {
            'alibaba': dwai_bailian_qa,
            'zhipu': zhipuai_chatglm_std,
            'huawei': pangu_completions,
            'minimax': mini_qa,
            'azure': azure_qa,
            'tencent': tione_chat_completion
        }

    def call(self, cloud, **kwargs):
        func = self.route_map.get(cloud)
        if func:
            return func(**kwargs)
        else:
            raise ValueError(f"Unknown cloud: {cloud}")


dwai.api_key = "dw-BBAa68XBJUqiIj6xUQcC0KREnqmt5mPKQ52wkylD-Tw"

if __name__ == '__main__':
    sdk = UnifiedSDK()
    print(">>>")

    data1 = """

        你是一个拥有丰富经验的SRE排障专家，请用中文与我沟通。
        我们现在遇到了一个故障：

        [故障描述]
        sls日志无法采集

        [历史CASE参考]
        问题描述: 业务反馈 algoqc-csprd-shoes-img-verify 应用刚上线，在阿里云后台配置的sls日志采集，从2023年08月14号中午一直没有日志展示
        ------------------------------------
        原因分析:
        原因1,该场景权重占比1%
        云商的logtail扫描没有过滤NAS卷的能力
        原因2,该场景权重占比2%
        业务方错误配置NAS卷挂载点，挂载到了/logs，被多台节点的logtail同时采集，造成IO阻塞
        ------------------------------------
        问题总结:部分业务把NAS卷挂载到了/logs目录，导致多台节点的logtail同时向NAS发起IO请求，出现了IO阻塞。logtail 导致日志采集无法正常工作。
        ------------------------------------
        解决方案:阿里云改造logtail能力，使之可以支持绕开NAS卷扫描，化解NAS扫描的IO压力

        [我的要求]
        请仔细参考这个case，请结合你多年的经验。帮我推断当前故障，值得排查的方向。
        尽可能以 Markdown 格式输出，排版要精美，避免不必要的换行。

      """
    data = """

    你是一个拥有丰富经验的SRE排障专家，请用中文与我沟通。
    我们现在遇到了一个故障：

    [故障描述]
    sls日志无法采集


    [历史CASE]：仅供参考

问题描述: 业务反馈 algoqc-csprd-shoes-img-verify 应用刚上线，在阿里云后台配置的sls日志采集，从2023年08月14号中午一直没有日志展示
------------------------------------
原因分析:
原因1,该场景权重占比1%
云商的logtail扫描没有过滤NAS卷的能力
原因2,该场景权重占比2%
业务方错误配置NAS卷挂载点，挂载到了/logs，被多台节点的logtail同时采集，造成IO阻塞
------------------------------------
问题总结:部分业务把NAS卷挂载到了/logs目录，导致多台节点的logtail同时向NAS发起IO请求，出现了IO阻塞。logtail 导致日志采集无法正常工作。
------------------------------------
解决方案:阿里云改造logtail能力，使之可以支持绕开NAS卷扫描，化解NAS扫描的IO压力


    [我的要求]
    请结合从前case和你多年的经验，进行深度思考。给出概率较高的详细 排障方向 和 解决思路。并且分别给出概率值！
    不用输出我的上下文，尽可能以 Markdown 格式输出，排版简洁美观

    """

    #
    # # 测试微软
    # resp = sdk.call('azure', model="gpt-35-turbo-16k", prompt=data, temperature=0.1)
    # re = resp.get("output").get("text")
    # print(re.replace("\\n", "\n"))

    # # 测试mini
    # resp = sdk.call('minimax', model="abab5.5-chat", prompt="你的参数量大概是多少？", temperature=0.1)
    # print(resp)
    #
    # # 测试dwai
    resp = sdk.call('alibaba', model="qwen-plus-v1", prompt="你的参数量大概是多少？")
    print(resp)

    # 测试zhipuai
    # resp = sdk.call('zhipu', model="chatglm_std", prompt=data, top_p=0.7, temperature=0.9)
    # re = resp.get("output").get("text")
    # print(re.replace("\\n", "\n"))

    #
    # # 测试pangu
    # resp = sdk.call('huawei', model="default", prompt="你的参数量大概是多少？", max_tokens=600, temperature=0.9)
    # print(resp)
    #
    # # 测试tione
    # resp = sdk.call('tencent', model="default", prompt="你的参数量大概是多少？")
    # print(resp)
