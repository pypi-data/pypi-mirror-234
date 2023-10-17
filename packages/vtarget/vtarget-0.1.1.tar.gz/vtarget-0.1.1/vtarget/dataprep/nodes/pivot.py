import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Pivot:
    def exec(self, flow_id: str, node_key: str, pin: dict, settings: dict):
        script = []
        # if node_key in cache_handler.cache[flow_id] and cache_handler.cache[flow_id][node_key]['config'] == json.dumps(settings, sort_keys=True):
        # 	bug_handler.console(f'Nodo "{node_key}" leído desde cache flow_id: "{flow_id}"', 'info', flow_id)
        # 	reset_childs = False
        # 	script_handler.script += cache_handler.cache[flow_id][node_key]['script']
        # 	return cache_handler.cache[flow_id][node_key]['pout'], reset_childs

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# PIVOT")
        # print(settings)

        # Definición de las funciones de agregación
        def concat(x, sep):
            return sep.join(x)

        # print(settings.keys())
        validation = list(
            set(["col_group", "col_header", "col_value", "agg_method"]) - set(settings.keys())
        )
        if len(validation) != 0:
            msg = (
                "(pivot_table): Debes completar todos los campos en la configuración. Campos faltantes: "
                + str(validation)
            )
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        # Obtengo las configuraciones
        col_group: list[str] = settings["col_group"] if "col_group" in settings else []
        col_header: str = settings["col_header"] if "col_header" in settings else ""
        col_value: str = settings["col_value"] if "col_value" in settings else ""
        agg_method: list[str] = settings["agg_method"] if "agg_method" in settings else []
        separator: str = settings["separator"] if "separator" in settings else ","

        agg_fn = []
        for am in agg_method:
            # if am == 'Concatenate': agg_fn.append(lambda x: concatenate(x, separator))
            if am in ["Concatenate", "Concat"]:

                def lmbd(x):
                    return concat(x, separator)

                lmbd.__name__ = "concat"
                agg_fn.append(lmbd)
            elif am == "Count (Without Nulls)":
                agg_fn.append(lambda x: len(x.dropna().unique()))
            elif am == "Count (With Nulls)":
                agg_fn.append("count")
            elif am == "Average":
                agg_fn.append("mean")
            else:
                agg_fn.append(am.lower())
        # print(agg_fn)
        # pivotea la tabla utilizando los métodos de agregación seleccionados
        try:
            # df = pd.pivot_table(df, index=groupby, columns=header, values=values, aggfunc=agg_fn, margins=True).reset_index()
            df = pd.pivot_table(
                df, index=col_group, columns=col_header, values=col_value, aggfunc=agg_fn
            ).reset_index()
        except Exception as e:
            msg = "(pivot_table) Exception:" + str(e)
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        # print(df.reset_index())
        df.columns = ["_".join(list(map(str, x))) if x[1] else x[0] for x in df.columns]
        script.append(
            "df = pd.pivot_table(df, index={}, columns={}, values={}, aggfunc={}).reset_index()".format(
                col_group, col_header, col_value, agg_fn
            )
        )
        script.append(
            'df.columns = ["_".join(list(map(str, x))) if x[1] else x[0] for x in df.columns ]'
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
