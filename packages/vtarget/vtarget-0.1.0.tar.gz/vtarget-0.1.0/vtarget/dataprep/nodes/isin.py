import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class IsIn:
    def exec(self, flow_id, node_key, pin, settings):
        script = []

        # if node_key in cache_handler.cache[flow_id] and cache_handler.cache[flow_id][node_key]['config'] == json.dumps(settings, sort_keys=True):
        # 	bug_handler.console(f'Nodo "{node_key}" leído desde cache flow_id: "{flow_id}"', 'info')
        # 	reset_childs = False
        # 	script_handler.script += cache_handler.cache[flow_id][node_key]['script']
        # 	return cache_handler.cache[flow_id][node_key]['pout'], reset_childs

        script_handler.script.append("\n# IS_IN")

        df_S: pd.DataFrame = pin["Src"].copy()
        df_V: pd.DataFrame = pin["Val"].copy()
        source: str = settings["source"]
        values: str = settings["values"]

        try:
            if "not_in" in settings and settings["not_in"]:
                df = df_S[~df_S[source].isin(df_V[values])].reset_index(drop=True)
            else:
                df = df_S[df_S[source].isin(df_V[values])].reset_index(drop=True)
            script_handler.script.append(
                "df = df[df_S[{}].isin(df_V[{}])].reset_index(drop=True)".format(source, values)
            )
        except Exception as e:
            msg = "(isin) Exception:" + str(e)
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
