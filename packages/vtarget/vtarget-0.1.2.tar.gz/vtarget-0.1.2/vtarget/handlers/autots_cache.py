import json

import pandas as pd

# from evalml.automl.automl_search import AutoMLSearch
from termcolor import colored

from vtarget.handlers.event_handler import event_handler


def find(arr, prop, value):
    for x in arr:
        if x[prop] == value:
            return x


class AutoTS_Cache:
    def __init__(self):
        self.df: pd.DataFrame = None
        self.basic_config: dict = None
        self.ts_quality = None
        self.series: list = []
        self.current_model_name: str = None
        self.current_serie_name: str = None
        self.autots_search = None

    def reset(self, key: str):
        pass

    def get_df(self):
        return self.df

    def get_series(self):
        return self.series

    def set_series(self, series: list):
        self.series = series

    def prepend_serie(self, serie: dict):
        self.series.insert(0, serie)

    def append_serie(self, serie: dict):
        self.series.append(serie)

    def prepend_model(self, model: dict, serie_name: str = None):
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        serie = self.find_serie(serie_name)
        if serie is not None:
            list(serie.models).insert(0, model)

    def append_model(self, model: dict, serie_name: str = None):
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        serie = self.find_serie(serie_name)
        if serie is not None:
            list(serie.models).append(model)

    def get_current_serie_name(self):
        return self.current_serie_name

    def set_current_serie_name(self, name: str):
        self.current_serie_name = name

    def is_a_serie_model(self, model_name: str, serie_name: str = None):
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        model = self.find_serie_model(serie_name, model_name)
        return model is not None

    def find_serie(self, serie_name: str) -> dict:
        return find(self.series, "name", serie_name)

    def find_serie_model(self, serie_name: str, model_name: str) -> dict:
        serie_name = find(self.series, "name", serie_name)
        if (
            serie_name is not None
            and serie_name["models"] is not None
            and len(serie_name["models"]) > 0
        ):
            return find(serie_name["models"], "name", model_name)

    def get_current_model_name(self):
        return self.current_model_name

    def set_current_model_name(self, name: str):
        self.current_model_name = name

    def set_serie_model_prop(
        self, prop: str, value: any, serie_name: str = None, model_name: str = None
    ):
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        if model_name is None:
            model_name = self.get_current_model_name()

        model = self.find_serie_model(serie_name, model_name)
        if model is not None:
            model[prop] = value
            # if prop == "status" and value == "IN_PROGRESS":
            #     self.set_current_model_name(model_name)
            event_handler.emit_queue.put(
                {
                    "name": "autots.update_model",
                    "data": json.dumps({"serie": serie_name, "model": model}, default=str),
                }
            )

    def update_serie_model(self, props: dict = {}, serie_name: str = None, model_name: str = None):
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        if model_name is None:
            model_name = self.get_current_model_name()
        model = self.find_serie_model(serie_name, model_name)
        if model is not None:
            model.update(props)
            event_handler.emit_queue.put(
                {
                    "name": "autots.update_model",
                    "data": json.dumps({"serie": serie_name, "model": model}, default=str),
                }
            )

    def update_serie(self, props: dict = {}, serie_name: str = None, send_to_view: bool = True):
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        serie = self.find_serie(serie_name)
        if serie is not None:
            serie.update(props)
            if send_to_view:
                event_handler.emit_queue.put(
                    {
                        "name": "autots.update_serie",
                        "data": json.dumps(
                            {k: v for k, v in serie.items() if k not in ["partition_data"]},
                            default=str,
                        ),
                    }
                )
        else:
            print(colored("NO EXISTE SERIE", "red", "on_white"))

    def get_serie_by_name(self, serie_name: str = None):
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        serie = self.find_serie(serie_name)
        return serie

    def get_serie_prop(self, prop: str, serie_name: str = None):
        if serie_name is None:
            serie_name = self.get_current_serie_name()
        serie = self.find_serie(serie_name)
        if serie is not None:
            if prop in serie:
                return serie[prop]
        return None

    def set_automl_search(self, automl):
        self.autots_search = automl

    def get_autots_search(self):
        return self.autots_search


autots_cache = AutoTS_Cache()
