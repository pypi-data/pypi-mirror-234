import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Cumsum:
    def exec(self, flow_id, node_key, pin, settings):
        script = []

        # if node_key in cache_handler.cache[flow_id] and cache_handler.cache[flow_id][node_key]['config'] == json.dumps(settings, sort_keys=True):
        # 	bug_handler.console(f'Nodo "{node_key}" leído desde cache flow_id: "{flow_id}"', 'info', flow_id)
        # 	reset_childs = False
        # 	script_handler.script += cache_handler.cache[flow_id][node_key]['script']
        # 	return cache_handler.cache[flow_id][node_key]['pout'], reset_childs

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# CUMSUM")
        # print(settings)
        groupby: list = settings["groupby"] if "groupby" in settings else []
        axis: str = settings["axis"] if "axis" in settings else None
        cumcount: bool = settings["cumcount"] if "cumcount" in settings else False
        cumsum: bool = settings["cumsum"] if "cumsum" in settings else False
        cumpct: bool = settings["cumpct"] if "cumpct" in settings else False
        pct: bool = settings["pct"] if "pct" in settings else False

        if not axis:
            msg = "(cumsum) Debes seleccionar una columna para aplicar la sumarización"
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        prefix = axis[:3]
        script.append(f"prefix = '{prefix}'")

        if not (cumcount or cumsum or cumpct or pct):
            msg = "(cumsum) No se seleccionó ninguna agregación para la columna seleccionada"
            return bug_handler.default_on_error(
                flow_id, node_key, msg, console_level="warn", bug_level="warning", success=True
            )

        try:
            if groupby:
                df_obj = df.groupby(groupby)
                script.append(f"df_obj = df.groupby({groupby})['{axis}']")
                if cumcount:
                    df[prefix + "_cumcount"] = df_obj.cumcount() + 1
                    script.append(f"df[prefix+'_cumcount'] = df_obj.cumcount()+1")
                if cumsum:
                    df[prefix + "_cumsum"] = df_obj[axis].apply(lambda x: x.cumsum())
                    script.append(f"df[prefix+'_cumsum'] = df_obj.apply(lambda x: x.cumsum())")
                if pct:
                    df[prefix + "_pct"] = df_obj[axis].apply(lambda x: x / x.sum())
                    script.append(f"df[prefix+'_pct'] = df_obj.apply(lambda x: x/x.sum())")
                if cumpct:
                    df[prefix + "_cumpct"] = df_obj[axis].apply(lambda x: (x / x.sum()).cumsum())
                    script.append(
                        f"df[prefix+'_cumpct'] = df_obj.apply(lambda x: (x/x.sum()).cumsum())"
                    )
            else:
                if cumcount:
                    df[prefix + "_cumcount"] = range(1, 1 + len(df))
                    script.append(f"df[prefix+'_cumcount'] = range(1, 1 + len(df))")
                if cumsum:
                    df[prefix + "_cumsum"] = df[axis].cumsum()
                    script.append(f"df[prefix+'_cumsum'] = df['{axis}'].cumsum()")
                if pct:
                    df[prefix + "_pct"] = df[axis] / df[axis].sum()
                    script.append(f"df[prefix+'_pct'] = df['{axis}']/df[axis].sum()")
                if cumpct:
                    df[prefix + "_cumpct"] = df[axis].cumsum() / df[axis].sum()
                    script.append(
                        f"df[prefix+'_cumpct'] = df['{axis}'].cumsum()/df['{axis}'].sum()"
                    )

        except Exception as e:
            msg = "(cumsum) Exception:" + str(e)
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
