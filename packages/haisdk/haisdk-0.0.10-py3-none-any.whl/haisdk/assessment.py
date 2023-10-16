import json

import os
import requests, io
import dill as pickle


class Assess:
    """
    Assess class is used to create an assessment

    Attributes
    ----------
    session : dict
    settings : dict -> {
        task: 'binary-classification' | 'clustering-efficacy' | 'simple-regression'
        target_column: '',
        prediction_column: '',
        prediction_proba_column: ''
    }
    """

    mandatory_settings_fields = ["task", "target_column"]
    mandatory_settings_tasks = {
        # target column or target columns
        "binary-classification": ["prediction_column", "prediction_proba_column"],
        "simple-regression": ["prediction_column"],
    }

    quant_assessment_url = (
        "https://apiv1.holisticai.com/api/v1/hai-assessments/efficacy/run"
    )
    # quant_assessment_url = "http://localhost:50051/api/v1/hai-assessments/efficacy/run"

    def __init__(self, session, settings):
        self.settings = settings
        self.session = session

    @staticmethod
    def _with_source():
        return (
            f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}"
            if "GITHUB_ACTIONS" in os.environ and os.environ["GITHUB_ACTIONS"] == "true"
            else "python-sdk"
        )

    def run(self, X, y, y_pred, model):
        either_model_or_predictions = (model is None) ^ (y_pred is None)
        if either_model_or_predictions is False:
            raise Exception("Either the model or y_pred should be present")
        config = self.session.config
        url = self.quant_assessment_url.replace("%s", config["clientId"])
        headers = {
            "apikey": "kp7k5diegu8uupx8j6vafulcxc4ygox94okbcnkyo",
            "content-type": "",
        }

        data = {
            "projectId": config["projectId"],
            "solutionId": config["solutionId"],
            "moduleId": config["moduleId"],
            "problemType": self.settings["task"],
            "dataType": self.settings["data_type"],
            "predictionColumns": self.settings["prediction_columns"],
            "targetColumns": self.settings["target_columns"],
            "modelClass": self.settings["model_class"],
            "train": X,
            "test": y,
            "model": model,
            "platformEndpoint": config["api"],
            "key": config["key"],
            "source": self._with_source(),
        }

        request_pkl = pickle.dumps(data)

        if y_pred is not None:
            y_pred_pkl = io.BytesIO()
            pickle.dump(y_pred, y_pred_pkl)
            data["predictions"] = y_pred_pkl

        res = requests.post(url=url, headers=headers, data=request_pkl)
        return res
