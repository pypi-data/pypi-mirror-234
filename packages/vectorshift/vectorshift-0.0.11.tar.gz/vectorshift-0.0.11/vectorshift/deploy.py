# functionality to deploy and run pipelines 
import requests

from pipeline import Pipeline
from consts import MODE

API_ENDPOINT = 'http://localhost:8000/api/pipelines/add' if MODE != 'PROD' else 'https://api.vectorshift.ai/api/pipelines/add'

class Config:
    # For now, the config is just a wrapper for the API key
    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def save_pipeline(self, pipeline: Pipeline):
        response = requests.post(
            API_ENDPOINT,
            data=({'pipeline': pipeline.to_json()}),
            headers={
                'Public-Key': self.public_key,
                'Private-Key': self.private_key
            }
        )

        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()
