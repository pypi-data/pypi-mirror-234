import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class InterRow:
    def __init__(self):
        self.map_timedelta = {
            "days": "D",
            "hours": "H",
            "minutes": "m",
            "seconds": "s",
        }

    def exec(self, flow_id, node_key, pin, settings):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# InterRow")

        # group_by, field, new_column_name, periods, fillna, fillna_value, fillna_value_timedelta
        groupby: list = settings["group_by"] if ("group_by" in settings and settings["group_by"] != []) else []
        field: str = settings["field"] if ("field" in settings and settings["field"] != "") else None
        new_column_name: str = (
            settings["new_column_name"]
            if ("new_column_name" in settings and settings["new_column_name"] != "")
            else "new_column"
        )

        periods: int = settings["periods"] if (("periods" in settings and settings["periods"] != "") or settings["periods"] == 0) else 0

        inter_row_type: str = (
            settings["inter_row_type"]
            if ("inter_row_type" in settings and settings["inter_row_type"] != "")
            else None
        )
        fillna: bool = (
            settings["fillna"] if ("fillna" in settings) else False
        )

        fillna_value : str = (
            settings["fillna_value"]
            if ("fillna_value" in settings and settings["fillna_value"] != "")
            else None
        )

        fillna_value_timedelta = (
            settings["fillna_value_timedelta"]
            if ("fillna_value_timedelta" in settings and settings["fillna_value_timedelta"] != {})
            else {}
        )

        if not field or (fillna and (not fillna_value and not fillna_value_timedelta)):
            if not field:
                msg = "(inter_row) Debes seleccionar al menos una columna para aplicar la función inter_row"
            if fillna and (not fillna_value and not fillna_value_timedelta):
                msg = "(inter_row) Si seleccionas la función 'fillna' debes especificar el valor para los nulos"

            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        try:
            query = ""
            if groupby:
                if fillna:
                    if fillna_value:
                        query = f"df.groupby(by=groupby)[[field]].{inter_row_type}(periods).fillna(fillna_value)"
                        df[new_column_name] = eval(query)
                    else:
                        query = f"df.groupby(by=groupby)[[field]].{inter_row_type}(periods).fillna(self.timedelta_parse(fillna_value_timedelta))"
                        df[new_column_name] = eval(query)
                else:
                    query = f"df.groupby(by=groupby)[[field]].{inter_row_type}(periods)"
                    df[new_column_name] = eval(query)
            else:
                if fillna:
                    if fillna_value:
                        query = f"df[[field]].{inter_row_type}(periods).fillna(fillna_value)"
                        df[new_column_name] = eval(query)
                    else:
                        query = f"df[[field]].{inter_row_type}(periods).fillna(self.timedelta_parse(fillna_value_timedelta))"
                        df[new_column_name] = eval(query)
                else:
                    query = f"df[field].{inter_row_type}(periods)"
                    df[new_column_name] = eval(query)

            script.append(f"df[{new_column_name}] = {query}")

        except Exception as e:
            msg = "(inter_row) Exception: " + str(e)
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

    def timedelta_parse(self, timedelta_data):
        return " ".join([str(value) + " " + key for key, value in timedelta_data.items()])
