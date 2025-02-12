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
        json_content = json.dumps(self.extracted_attributes, indent=2)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in urban sustainability and green infrastructure planning. Your task is to assess a site's suitability for green infrastructure based on various environmental factors."},
                {"role": "user", "content": f"Given the following site data:\n\n{json_content}\n\nProvide an insightful summary assessing the potential for implementing green infrastructure. Discuss factors such as flood risk, urban heat mitigation, soil suitability, and social considerations."}
            ]
        )

        self.logger.info(completion.choices[0].message)
        return completion.choices[0].message
