import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Melt:
    def exec(self, flow_id, node_key, pin, settings):
        script = []

        # if node_key in cache_handler.cache[flow_id] and cache_handler.cache[flow_id][node_key]['config'] == json.dumps(settings, sort_keys=True):
        # 	bug_handler.console(f'Nodo "{node_key}" leído desde cache flow_id: "{flow_id}"', 'info')
        # 	reset_childs = False
        # 	script_handler.script += cache_handler.cache[flow_id][node_key]['script']
        # 	return cache_handler.cache[flow_id][node_key]['pout'], reset_childs

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# MELT")

        # Obtengo las configuraciones
        id_vars: list[str] = settings["id_vars"]
        value_vars: list[str] = settings["value_vars"]

        # transpone multiples columnas dejandolas en una sola columna con variables categoricas
        try:
            df = pd.melt(df, id_vars=id_vars, value_vars=value_vars).reset_index(drop=True)
        except Exception as e:
            msg = "(melt) Exception:" + str(e)
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        script.append(
            "df = pd.melt(df, id_vars={}, value_vars={}).reset_index(drop=True)".format(
                id_vars, value_vars
            )
        )

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
