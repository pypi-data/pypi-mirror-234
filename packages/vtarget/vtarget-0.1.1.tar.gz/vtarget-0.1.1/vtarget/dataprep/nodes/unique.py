import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Unique:
    def exec(self, flow_id, node_key, pin, settings):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Unique")

        # field
        field: list = (
            settings["field"] if ("field" in settings and settings["field"] is not None) else []
        )
        # print(field)
        if not field:
            msg = "(unique) Debes seleccionar al menos una columna para aplicar la función unique"
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        try:
            df = df.groupby(field).size().reset_index().drop(columns=[0])
            script.append(
                "df = df.groupby({}).size().reset_index().drop(columns=[0])".format(field)
            )
            # new_df = pd.DataFrame()
            # script.append('new_df = pd.DataFrame()')
            # new_df[field] = df[field].unique()
            # script.append('new_df[{}] = df[{}].unique()'.format(field, field))
        except Exception as e:
            msg = "(unique) Exception:" + str(e)
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
