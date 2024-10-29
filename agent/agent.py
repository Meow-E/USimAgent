import json
from config.config import *
from langchain_core.prompts import PromptTemplate
from openai import OpenAI
import httpx


class Agent:
    def __init__(self, prompt, **kwargs):
        self.prompt = PromptTemplate.from_template(prompt).format(**kwargs)
        self.client = OpenAI(
            base_url=API_BASE,
            api_key=API_KEY,
            http_client=httpx.Client(
                base_url=API_BASE,
                follow_redirects=True
            )
        )

    @staticmethod
    def normalize_json(result):
        # json的最前面有```json字样，把该字样删掉
        # example: ```json {"result": "result"} —> {"result": "result"}
        if result[0] != '{' or result[-1] != '}':
            first_index = result.find('{')
            last_index = result.rfind('}')
            result = result[first_index: last_index + 1]

        # 大括号用{{ }}表示，改为{}
        # example: {{"result": "result"}} —> {{"result": "result"}}
        result = result.replace("{{", "{").replace("}}", "}")

        # 有多于两个json，只取第一个
        # example: {"result": "result1"}, {"result": "result2"} —> {"result": "result1"}
        if result.count('{') > 1 or result.count('}') > 1:
            index = result.find('}')
            result = result[:index + 1]

        # 最后一位的后面有逗号，把逗号删掉
        # example: {"result": "result",} —> {"result": "result"}
        last_index1 = result.rfind(',')
        last_index2 = result.rfind('"')
        if last_index1 > last_index2:
            result = result[:last_index1] + result[last_index1 + 1:]

        # 返回一些非法组合
        # example: }\n} -> }
        result = result.replace("}\n}", "}")

        return result

    def generate(self):
        result = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": self.prompt}],
            temperature=TEMPERATURE,
            n=1
        ).choices[0].message.content.strip()

        print('Prompt: \n' + self.prompt)
        print('=======================')
        print('Response: \n' + result)
        try:
            result_json = json.loads(result)
        except:
            result = Agent.normalize_json(result)

            if 'click' in result:
                result = result[:5] + result[5:-2].replace("{", "").replace("}", "") + result[-2:]

            result_json = json.loads(result)

        return result_json
