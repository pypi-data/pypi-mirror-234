import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Concat:
    def exec(self, flow_id, node_key, pin, settings):
        script = []

        # if node_key in cache_handler.cache[flow_id] and cache_handler.cache[flow_id][node_key]['config'] == json.dumps(settings, sort_keys=True):
        # 	bug_handler.console(f'Nodo "{node_key}" leído desde cache flow_id: "{flow_id}"', 'info', flow_id)
        # 	reset_childs = False
        # 	script_handler.script += cache_handler.cache[flow_id][node_key]['script']
        # 	return cache_handler.cache[flow_id][node_key]['pout'], reset_childs

        script.append("\n# CONCAT")
        df_A: pd.DataFrame = pin["A"].copy()
        df_B: pd.DataFrame = pin["B"].copy()
        selected_A: list = settings["a"] if "a" in settings and settings["a"] is not None else None
        selected_B: list = settings["b"] if "b" in settings and settings["b"] is not None else None

        # print(df_A.columns)
        # print(df_B.columns)

        if not selected_A:
            msg = "(concat): Debes mantener al menos un campo en el puerto A"
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        df_A = df_A[selected_A]
        script.append("df_A = df_A[{}]".format(selected_A))

        # Me quedo con los campos seleccionados del Source
        if not selected_B:
            msg = "(concat): Debes mantener al menos un campo en el puerto B"
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        df_B = df_B[selected_B]
        script.append("df_B = df_B[{}]".format(selected_B))

        try:
            df = pd.concat([df_A, df_B], ignore_index=True)
            script.append("df = pd.concat([df_A, df_B], ignore_index=True)")
        except Exception as e:
            msg = "(concat) Exception:" + str(e)
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
