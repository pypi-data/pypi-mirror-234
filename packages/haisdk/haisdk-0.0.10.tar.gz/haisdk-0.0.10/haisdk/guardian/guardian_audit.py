import requests

class GuardianAudit:

    guardian_base_url = (
        "https://apiv1.holisticai.com/api/v1/shield-protection/audit"
    )
    prompts_endpoint = "/unauthenticated/prompts"
    run_audit_endpoint = "/unauthenticated/run-audit"


    def __init__(self, config):
        self.config = config
        self.validate_config(config)

    @staticmethod
    def validate_config(config):
        if "apikey" not in config:
            raise Exception("Expected apikey does not exist in the provided config")
        if "audit_id" not in config:
            raise Exception("Expected api name does not exist in the provided config")

    # hardcoded only for stereotype prompts
    def load_prompts(self):
        url = self.guardian_base_url + self.prompts_endpoint + f"/{self.config['tenant_id']}/{self.config['audit_id']}"
        headers = {
            "x-hai-guardian-key": self.config["apikey"],
            "apikey": "918vz18ncjupyl4wl8ocxhanrzy2gvr51b9qo98pk",
        }
        response = requests.get(url=url, headers=headers)
        return response.json()

    def process(self, data):
        url = self.guardian_base_url + self.run_audit_endpoint
        headers = {
            "x-hai-guardian-key": self.config["apikey"],
            "apikey": "918vz18ncjupyl4wl8ocxhanrzy2gvr51b9qo98pk",
        }
        json_data = {
            "tenant_id": self.config["tenant_id"],
            "audit_id": self.config["audit_id"],
            "apikey": self.config["apikey"],
            "messages": data
        }
        response = requests.post(url=url, headers=headers, json=json_data)
        print(response)
