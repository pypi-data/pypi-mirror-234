import abc
import json
from datetime import datetime
from abc import ABC
from tketool.utils.LocalRedis import *
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from typing import Optional, List, Dict, Mapping, Any
import requests, openai, os
from tketool.logs import log_debug


def add_token_use(model_name, use: (int, int), prices: (int, int)):
    now = datetime.now()
    date_time_str = now.strftime("%m_%d")
    keyname = f"lm_{date_time_str}_{model_name}"

    if not has_value(keyname):
        set_value(keyname, 0)
        set_value(keyname + "_use_in", 0)
        set_value(keyname + "_use_out", 0)
        set_value(keyname + "_use_in_price", prices[0])
        set_value(keyname + "_use_out_price", prices[1])

    value_add(keyname + "_use_in", use[0])
    value_add(keyname + "_use_out", use[1])

    current_cost = get_value(keyname + '_use_in') / 1000 * prices[0] + prices[1] / 1000 * get_value(
        keyname + '_use_out')

    log_debug(f"{model_name} add token:{use[0]}/{use[1]}"
              f" totle {get_value(keyname + '_use_in')}/{get_value(keyname + '_use_out')} "
              f" cost {round(current_cost, 2)}"
              f"")


class LLM_Plus(LLM):
    @abc.abstractmethod
    def _call(self, prompt: str, stop: Optional[List[str]] = None,
              run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any) -> str:
        pass

    @property
    @abc.abstractmethod
    def _llm_type(self) -> str:
        pass

    @abc.abstractmethod
    def state(self) -> dict:
        pass


class ChatGLM(LLM):
    gurl = ""

    def __init__(self, _url):
        super().__init__()
        self.gurl = _url

    @property
    def _llm_type(self) -> str:
        return "chatglm"

    def _construct_query(self, prompt: str) -> Dict:
        """构造请求体
        """
        query = {
            "prompt": prompt,
            "history": []
        }
        return query

    @classmethod
    def _post(cls, url: str,
              query: Dict) -> Any:
        """POST请求
        """

        _headers = {"Content_Type": "application/json"}
        with requests.session() as sess:
            resp = sess.post(url,
                             json=query,
                             headers=_headers,
                             timeout=60)

        return resp

    def _call(self, prompt: str,
              stop: Optional[List[str]] = None) -> str:
        """_call
        """
        # construct query
        query = self._construct_query(prompt=prompt)

        # post
        resp = self._post(url=self.gurl,
                          query=query)

        if resp.status_code == 200:
            resp_json = resp.json()
            predictions = resp_json["response"]

            return predictions
        else:
            return "请求模型"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters.
        """
        _param_dict = {
            "url": self.gurl
        }
        return _param_dict


class ChatGPT4(LLM_Plus):
    def state(self) -> dict:
        return {
            'api_token': self.api_token[:5] + "*****" + self.api_token[-5:],
            'model_name': self.model_name,
            'proxy': self.proxy
        }

    api_token = ""
    temperature = 0.8
    model_name = "gpt-4"
    proxy = ""

    def __init__(self, apitoken, proxy=None, temperature=0.8):
        super().__init__()
        self.api_token = apitoken
        self.temperature = temperature
        openai.api_key = self.api_token
        self.proxy = proxy
        if proxy is not None:
            # os.environ['OPENAI_API_PROXY'] = ""
            openai.proxy = proxy  # "192.168.2.1:9999"

    @property
    def _llm_type(self) -> str:
        return "chatgpt-4"

    def _construct_query(self, prompt: str) -> List:
        """构造请求体
        """
        query = [
            {"role": "user", "content": prompt}
        ]
        return query

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        """_call
        """
        message = self._construct_query(prompt)

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=message,
        )

        answer = response.choices[0]['message']['content']

        prompt_token_count = response['usage']['prompt_tokens']
        completion_token_count = response['usage']['completion_tokens']

        add_token_use(self.model_name, (prompt_token_count, completion_token_count), (0.03, 0.06))

        return answer

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters.
        """
        _param_dict = {

        }
        return _param_dict


class ChatGPT3(LLM_Plus):
    def state(self) -> dict:
        return {
            'api_token': self.api_token[:5] + "*****" + self.api_token[-5:],
            'model_name': self.model_name,
            'proxy': self.proxy
        }

    api_token = ""
    temperature = 0.8
    model_name = "gpt-3.5-turbo-0613"
    proxy = ""

    def __init__(self, apitoken, proxy=None, temperature=0.8):
        super().__init__()
        self.api_token = apitoken
        self.temperature = temperature
        openai.api_key = self.api_token
        self.proxy = proxy
        if proxy is not None:
            # os.environ['OPENAI_API_PROXY'] = ""
            openai.proxy = proxy  # "192.168.2.1:9999"

    @property
    def _llm_type(self) -> str:
        return self.model_name

    def _construct_query(self, prompt: str) -> List:
        """构造请求体
        """
        query = [
            {"role": "user", "content": prompt}
        ]
        return query

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        """_call
        """
        message = self._construct_query(prompt)

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=message,
        )

        answer = response.choices[0]['message']['content']

        prompt_token_count = response['usage']['prompt_tokens']
        completion_token_count = response['usage']['completion_tokens']

        add_token_use(self.model_name, (prompt_token_count, completion_token_count), (0.0015, 0.002))
        return answer

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters.
        """
        _param_dict = {

        }
        return _param_dict
