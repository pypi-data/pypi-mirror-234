import json

import pandas as pd

from evalml.automl.automl_search import AutoMLSearch
from vtarget.handlers.event_handler import event_handler


def find(arr: list, prop: str, value: any):
    for x in arr:
        if x[prop] == value:
            return x


class AutoML_Cache:
    def __init__(self):
        self.df: pd.DataFrame = None
        self.target: str = None
        self.problem_type: str = None
        self.models: list = []
        self.current_model_name: str = None
        self.partition_data: dict = {}
        self.automl_search: AutoMLSearch = None

    def reset(self):
        pass

    def find_model(self, model_name: str) -> dict:
        return find(self.models, "name", model_name)

    def get_df(self):
        return self.df

    def set_models(self, models: list):
        self.models = models
        event_handler.emit_queue.put(
            {
                "name": "automl.set_models",
                "data": json.dumps(models, default=str),
            }
        )

    def prepend_model(self, model: dict):
        self.models.insert(0, model)

    def append_model(self, model: dict):
        self.models.append(model)

    def is_a_model(self, model_name: str):
        model = self.find_model(model_name)
        return model is not None

    def get_current_model_name(self):
        return self.current_model_name

    def set_current_model_name(self, name: str):
        self.current_model_name = name

    def update_model(self, props: dict = {}, model_name: str = None):
        if model_name is None:
            model_name = self.get_current_model_name()
        model = self.find_model(model_name)
        if model is not None:
            model.update(props)
            event_handler.emit_queue.put(
                {
                    "name": "automl.update_model",
                    "data": json.dumps(model, default=str),
                }
            )

    # def update_models(self, models: list = []):
    #     for m in models:

    def get_partition_data(self) -> dict:
        return self.partition_data

    def set_partition_data(self, data: dict = {}):
        # self.partition_data.update(data)
        self.partition_data = data

    def set_automl_search(self, automl: AutoMLSearch):
        self.automl_search = automl

    def get_automl_search(self) -> AutoMLSearch:
        return self.automl_search


automl_cache = AutoML_Cache()
