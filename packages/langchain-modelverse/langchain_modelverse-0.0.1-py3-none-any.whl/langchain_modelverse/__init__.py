import json
import re
from typing import Optional, List, Any, Mapping
import requests
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM


class ModelVerseAI(LLM):
    streaming: bool = False

    _ENDPOINT_URL = "https://model-verse.fly.dev/prompt"

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")

        headers = {
            "Accept": "text/plain" if self.streaming else "application/json",
            "Content-Type": "application/json",
        }

        data = {
            "history": kwargs["history"] if "history" in kwargs else [],
            "prompt": prompt,
            "stream": 1 if self.streaming else 0,
        }

        session = requests.Session()
        resp = session.post(url=ModelVerseAI._ENDPOINT_URL, headers=headers, data=json.dumps(data), stream=self.streaming)

        if self.streaming:
            output = ""
            retval = ""
            for ch in resp.iter_content():
                output += ch.decode('UTF-8')

                pattern = r'data: (.*)\r\n'
                match = re.search(pattern, output)
                if match:
                    generated = match.group(1)
                    retval += generated
                    run_manager.on_llm_new_token(generated)

                    output = ""

            return retval
        else:
            return resp.json()["data"]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}
