import openai
from openai import Completion

class GPTWrapper:

    def __init__(self):
        self.model = "gpt-3.5-turbo-instruct"
        openai.api_key = "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"

    def complete(self, prompt
                 ):
        return Completion.create(
            model=self.model,
            prompt=prompt,
            stop = ["."]
        )