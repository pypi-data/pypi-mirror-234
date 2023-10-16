import json

import requests


class GuardianProcessor:
    """
    {
        "tenant_id": "",
        "apikey": "",
        "api_name": ""
    }
    """

    guardian_base_url = (
        "https://apiv1.holisticai.com/api/v1/shield-protection/integration"
    )
    analyse_endpoint = "/unauthenticated/messages/analyse"
    analyse_async_endpoint = "/unauthenticated/messages/analyse-async"

    def __init__(self, config):
        self.config = config
        self.validate_config(config)

    @staticmethod
    def validate_config(config):
        if "apikey" not in config:
            raise Exception("Expected apikey does not exist in the provided config")
        if "api_name" not in config:
            raise Exception("Expected api name does not exist in the provided config")

    @staticmethod
    def validate_request(json_data):
        if "data" not in json_data:
            raise Exception(
                "Expected field data does not exist in the provided json_data"
            )
        if "message_groups" not in json_data["data"]:
            raise Exception(
                "Expected field message_groups does not exist in the provided data"
            )
        if len(json_data["data"]["message_groups"]) > 50:
            raise Exception(
                "Expected field message_groups exceeds the limit of 50 messages"
            )
        if len(json_data["data"]["message_groups"]) % 2 != 0:
            raise Exception(
                "Expected field message_groups should be grouped in batches of size 2"
            )

    def prepare_request(self, json_data, endpoint):
        url = self.guardian_base_url + endpoint
        headers = {
            "x-hai-guardian-key": self.config["apikey"],
            "apikey": "918vz18ncjupyl4wl8ocxhanrzy2gvr51b9qo98pk",
        }
        json_data["tenant_id"] = self.config["tenant_id"]
        json_data["api_name"] = self.config["api_name"]
        return url, headers, json_data

    def analyse(self, json_data):
        """Analysis the messages, registers and processes them async"""
        self.validate_request(json_data)

        url, headers, json_data = self.prepare_request(json_data, self.analyse_endpoint)
        response = requests.post(url=url, headers=headers, json=json_data)
        if response.status_code != 200:
            raise Exception(
                f"Registering messages in batch failed with status code {response.status_code}"
            )
        return json.loads(response.content)

    def analyse_async(self, json_data):
        """Analysis the messages, registers and processes them async"""
        self.validate_request(json_data)

        url, headers, json_data = self.prepare_request(json_data, self.analyse_async_endpoint)
        response = requests.post(url=url, headers=headers, json=json_data)
        if response.status_code != 200:
            raise Exception(
                f"Registering messages in batch failed with status code {response.status_code}"
            )
