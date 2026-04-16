# core/llm_client.py

import requests

class LLMClient:
    def __init__(self, api_url, api_key=None):
        self.api_url = api_url
        self.api_key = api_key

    def generate(self, prompt):
        try:
            response = requests.post(
                self.api_url,
                json={"prompt": prompt},
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return response.json().get("text", "")
        except:
            return "fallback response"