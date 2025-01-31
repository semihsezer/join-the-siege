import requests
import os
from copy import deepcopy
from functools import cached_property


DEFAULT_PAYLOAD = {
    "model": "llama-3.1-sonar-small-128k-online",
    "messages": [
        {
            "role": "system",
            "content": "You are an AI assistant that always responds in valid JSON format. You will receive some text and be asked to classify it into one of the given categories. Your responses should be structured as {'classification': '<classification_category>'}, where <classification_category> is one of the provided categories."
        },
    ],
    "max_tokens": 200,
}


class PerplexityClient:
    def __init__(self):
        self.url = "https://api.perplexity.ai/chat/completions"

    @cached_property
    def headers(self):
        token = os.getenv("PERPLEXITY_API_TOKEN")
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def get_payload(self, prompt):
        payload = deepcopy(DEFAULT_PAYLOAD)
        payload["messages"].append({"role": "user", "content": prompt})
        return payload

    def generate(self, prompt: str) -> str:
        print("Generating AI response...")
        payload = self.get_payload(prompt)

        response = requests.request(
            "POST", self.url, json=payload, headers=self.headers
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return content