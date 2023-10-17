import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class ValueCounts:
    def exec(self, flow_id: str, node_key: str, pin: dict, settings: dict):
        script = []
        # if node_key in cache_handler.cache[flow_id] and cache_handler.cache[flow_id][node_key]['config'] == json.dumps(settings, sort_keys=True):
        # 	bug_handler.console(f'Nodo "{node_key}" leído desde cache flow_id: "{flow_id}"', 'info', flow_id)
        # 	reset_childs = False
        # 	script_handler.script += cache_handler.cache[flow_id][node_key]['script']
        # 	return cache_handler.cache[flow_id][node_key]['pout'], reset_childs

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# VALUE_COUNTS")
        if "field" not in settings:
            msg = "(value_counts) Debes seleccionar un columna para el campo Field"
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        field: str = settings["field"]
        ascending: bool = (
            settings["ascending"]
            if ("ascending" in settings and settings["ascending"] is not None)
            else True
        )
        drop_na: bool = (
            settings["drop_na"]
            if ("drop_na" in settings and settings["drop_na"] is not None)
            else False
        )
        # normalize: bool = (
        #     settings["normalize"]
        #     if ("normalize" in settings and settings["normalize"] is not None)
        #     else False
        # )
        # print(field, ascending, drop_na, normalize)

        try:
            df_pct = df.value_counts(subset=field, normalize=True, ascending=ascending, dropna=drop_na)
            df_pct = df_pct.reset_index(name="value_pct")
            
            df_count = df.value_counts(subset=field, normalize=False, ascending=ascending, dropna=drop_na)
            df_count = df_count.reset_index(name="value_count")
            
            df = pd.merge(df_count, df_pct)
            
            script.append("\n# pct data")
            script.append("df_pct = df.value_counts(subset=[{}], normalize=True, ascending={}, dropna={})".format(field, ascending, drop_na))
            script.append("df_pct = df_pct.reset_index(name='value_pct')")
            
            script.append("\n# count data")
            script.append("df_count = df.value_counts(subset=[{}], normalize=False, ascending={}, dropna={})".format(field, ascending, drop_na))
            script.append("df_count = df_count.reset_index(name='value_count')")
            
            script.append("\n# merge data")
            script.append("df = pd.merge(df_count, df_pct)")
            
        except Exception as e:
            msg = "(value_counts) Exception:" + str(e)
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
