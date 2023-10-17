import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class DatetimeExtract:
    def __init__(self):
        pass

    def exec(self, flow_id, node_key, pin, settings):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Datetime Extract")

        items: list[str] = ( settings["items"] if ("items" in settings and settings["items"] is not None) else None)

        if items:
            for item in items:
                # column_to_convert, new_column_name, to_extract
                column_to_convert: str = ( item["column_to_convert"] if ("column_to_convert" in item and item["column_to_convert"] != '') else '')
                to_extract: str = ( item["to_extract"] if ("to_extract" in item and item["to_extract"] != '') else '')
                new_column_name: str = item["new_column_name"] if "new_column_name" in item and item["new_column_name"] != '' else to_extract.replace("()", "")

                msg: str = None
                if not to_extract: msg = "(datetime_extract) Debes seleccionar al menos un campo a obtener para aplicar la función DateTime Extract"
                if not column_to_convert: msg = "(datetime_extract) Debes seleccionar al menos una columna para aplicar la función DateTime Extract"
                if msg: return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

                try:
                    # Forma 1
                    df[new_column_name] = eval("df[column_to_convert].dt.{}".format(to_extract))
                    script.append(f'df["{new_column_name}"] = df[column_to_convert].dt.{to_extract}')

                except Exception as e:
                    msg = "(datetime_extract) Exception:" + str(e)
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
        else:
            return bug_handler.default_on_error(flow_id, node_key, "(datetime_extract) Debes seleccionar al menos una columna para aplicar la función DateTime Extract", console_level="error")
