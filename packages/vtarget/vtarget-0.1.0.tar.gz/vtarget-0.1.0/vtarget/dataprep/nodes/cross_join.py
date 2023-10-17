import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class CrossJoin:
    def exec(self, flow_id, node_key, pin, settings):
        script = []

        # if node_key in cache_handler.cache[flow_id] and cache_handler.cache[flow_id][node_key]['config'] == json.dumps(settings, sort_keys=True):
        # 	bug_handler.console(f'Nodo "{node_key}" leído desde cache flow_id: "{flow_id}"', 'info', flow_id)
        # 	reset_childs = False
        # 	script_handler.script += cache_handler.cache[flow_id][node_key]['script']
        # 	return cache_handler.cache[flow_id][node_key]['pout'], reset_childs

        script.append("\n# CROSS_JOIN")
        df_T: pd.DataFrame = pin["Tgt"].copy()
        df_S: pd.DataFrame = pin["Src"].copy()

        # Me quedo con los campos seleccionados del Target
        # selected_T = dict(filter(lambda x: x[1]['selected'], dtypes['Tgt']['dtypes'].items()))
        selected_T: list = settings["tgt"] if "tgt" in settings else []
        if not selected_T:
            msg = "(cross_join) Debes mantener al menos un campo en la entrada Target"
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        df_T = df_T[selected_T]
        script.append("df_T = df_T[{}]".format(selected_T))

        # Me quedo con los campos seleccionados del Source
        # selected_S = dict(filter(lambda x: x[1]['selected'], dtypes['Src']['dtypes'].items()))
        selected_S: list = settings["src"] if "src" in settings else []
        if not selected_S:
            msg = "(cross_join) Debes mantener al menos un campo en la entrada Source"
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        df_S = df_S[selected_S]
        script.append("df_S = df_S[{}]".format(selected_S))

        try:
            df = pd.merge(df_T, df_S, how="cross")  # , validate="many_to_one")
            script.append("df = pd.merge(df_T, df_S, how='cross')")
        except Exception as e:
            msg = "(cross_join) Exception:" + str(e)
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
