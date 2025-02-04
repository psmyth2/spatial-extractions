from openai import OpenAI
import json
import logging
import common


class Summarize:
    def __init__(self, structured_json: json):
        self.logger = logging.getLogger(__name__)
        self.config = common.get_config_parser()
        self.extracted_attributes = structured_json
        self.api_key = self.config['openai']['openai-api-key']

    def get_response(self):
        client = OpenAI(api_key=self.api_key)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": "Write a haiku about recursion in programming."
                }
            ]
        )

        self.logger.info(completion.choices[0].message)
