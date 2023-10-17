import datetime
import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class DatetimeFormatter:
    # def __init__(self):
    # self.pattern = re.compile(
    #     r"day|dd|Month|Mon|MM|yyyy|yy|hh|HH|mm|ss|,|\.|-|:|;|/|\||\s|de|las|a"
    # )
    # self.map_datetime = {
    #     "dy": "%j",
    #     "day": "%A",
    #     "dd": "%d",
    #     "Month": "%B",
    #     "Mon": "%b",
    #     "MM": "%m",
    #     "yy": "%y",
    #     "yyyy": "%Y",
    #     "HH": "%I",
    #     "hh": "%H",
    #     "mm": "%M",
    #     "ss": "%S",
    #     ",": ",",
    #     ".": ".",
    #     "-": "-",
    #     ":": ":",
    #     ";": ";",
    #     "/": "/",
    #     "|": "|",
    #     " ": " ",
    #     "de": "de",
    #     "las": "las",
    #     "a": "a",
    # }

    def exec(self, flow_id, node_key, pin, settings):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Datetime Formatter")

        # column_to_convert, new_column_name, pattern, custom_pattern
        column_to_convert: str = (
            settings["column_to_convert"]
            if "column_to_convert" in settings and settings["column_to_convert"] != None
            else None
        )
        new_column_name: str = (
            settings["new_column_name"]
            if "new_column_name" in settings and settings["new_column_name"] != ""
            else "new_column_name"
        )
        pattern: str = (
            settings["pattern"] if "pattern" in settings and settings["pattern"] != None else None
        )
        custom_pattern: str = (
            settings["custom_pattern"]
            if "custom_pattern" in settings and settings["custom_pattern"] != None
            else None
        )

        if not column_to_convert:
            msg = "(datetime_formatter) Debes seleccionar al menos una columna para aplicar la función DateTime Formatter"
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        if custom_pattern:
            if custom_pattern[0] not in ["'", '"'] or custom_pattern[-1] not in ["'", '"']:
                msg = "(datetime_formatter) El patrón personalizado debe venir entre comillas"
                return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
            pattern = custom_pattern[1:-1]
        else:
            if not pattern:
                msg = "(datetime_formatter) Debes seleccionar al menos un formato para aplicar la función DateTime Formatter"
                return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
            # pattern = pattern[1:-1]

        try:
            script.append(
                f"""df["{new_column_name}"] = df.apply(lambda x: process_datetime(x["{column_to_convert}"], "{pattern}"), axis=1)"""
            )

            df[new_column_name] = df.apply(
                lambda x: self.process_datetime(x[column_to_convert], pattern, script), axis=1
            )

        except Exception as e:
            msg = "(datetime_formatter) Exception:" + str(e)
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache', "info", flow_id)
        script_handler.script += script
        return {"Out": df}

    def process_datetime(self, _datetime, pattern, script):
        # Hay que ver por qué ocurren estos 2 casos
        # Cuando es string entra como None
        if isinstance(_datetime, float):
            return None
        # Cuando es datetime entra como NaT
        if pd.isnull(_datetime):
            return None
        if not _datetime:
            return None

        result = _datetime
        # Es string
        if isinstance(_datetime, str):
            result = datetime.datetime.strptime(_datetime.lower(), pattern)
            if len(script) == 2:
                script.append(
                    f"""def process_datetime(_datetime, pattern): \n\treturn datetime.datetime.strptime(_datetime.lower(), pattern)"""
                )
        else:
            result = _datetime.strftime(pattern)
            if len(script) == 2:
                script.append(
                    f"""def process_datetime(_datetime, pattern): \n\treturn _datetime.strftime(pattern)"""
                )

        return result

    # def validate_custom_format(self, custom_pattern):
    #     new_pattern = ""
    #     matches = self.pattern.finditer(custom_pattern)
    #     for match in matches:
    #         pattern = self.get_datetime_pattern(match.group())
    #         if not pattern:
    #             return None
    #         else:
    #             new_pattern += pattern
    #         # print("Coincidencia:", match.group())
    #         # print("Posición inicial:", match.start())
    #         # print("Posición final:", match.end())
    #     return new_pattern

    # def get_datetime_pattern(self, pattern):
    #     return self.map_datetime[pattern] if pattern in self.map_datetime else None
