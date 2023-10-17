import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Sort:
    def exec(self, flow_id, node_key, pin, settings):
        script = []
        # sufix_in = settings['port_In']

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# SORT")
        setting_list = list(map(lambda x: (x["field"], int(x["ascending"])), settings["items"]))
        columns, order = zip(*setting_list)

        try:
            df = df.sort_values(by=list(columns), ascending=list(order))
            script.append(
                "df_{} = df.sort_values(by=list({}), ascending=list({}))".format(
                    node_key, columns, order
                )
            )
        except Exception as e:
            msg = "(sort) Exception:" + str(e)
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
