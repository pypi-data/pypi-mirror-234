import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Describe:
    def exec(self, flow_id, node_key, pin, settings):
        script = []
        # if node_key in cache_handler.cache[flow_id] and cache_handler.cache[flow_id][node_key]['config'] == json.dumps(settings, sort_keys=True):
        # 	bug_handler.console(f'Nodo "{node_key}" leído desde cache flow_id: "{flow_id}"', 'info', flow_id)
        # 	reset_childs = False
        # 	script_handler.script += cache_handler.cache[flow_id][node_key]['script']
        # 	return cache_handler.cache[flow_id][node_key]['pout'], reset_childs

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# DESCRIBE")

        all_: str = "all"  # TODO: recibir desde la config
        groupby: list = (
            settings["groupby"] if ("groupby" in settings and settings["groupby"] is not []) else []
        )
        fields: list = (
            settings["fields"] if ("fields" in settings and settings["fields"] is not None) else []
        )
        percentiles: list = (
            settings["percentiles"]
            if ("percentiles" in settings and settings["percentiles"] is not None)
            else []
        )
        custom_percentiles: list = (
            settings["custompercentiles"]
            if ("custompercentiles" in settings and settings["custompercentiles"] is not None)
            else []
        )

        if "pivot_data" not in settings:
            settings["pivot_data"] = True

        pivot_data: bool = (
            settings["pivot_data"]
            if ("pivot_data" in settings and settings["pivot_data"] is not None)
            else True
        )

        if not fields:
            msg = "(describe) Debes seleccionar al menos una columna para aplicar el describe"
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        fields = list(filter(lambda x: x in df.columns, fields))
        all_percentiles = percentiles + custom_percentiles
        # quitar percentiles repetidos
        if type(all_percentiles) is list and len(all_percentiles) > 0:
            all_percentiles = list(set(all_percentiles))

        try:
            if groupby:
                df = (
                    df.groupby(by=groupby)[fields]
                    .describe(include=all_, percentiles=all_percentiles)
                    .reset_index()
                )
                script.append(
                    "df = df.groupby(by={})[{}].describe(include='{}', percentiles={}).reset_index()".format(
                        groupby, fields, all_, all_percentiles
                    )
                )

                if len(fields) > 1:
                    df.columns = ["_".join(list(map(str, x))) if x[1] else x[0] for x in df.columns]
                    script.append(
                        "df.columns = ['_'.join(list(map(str, x))) if x[1] else x[0] for x in df.columns]"
                    )
                else:
                    df.columns = [x[1] if x[1] else x[0] for x in df.columns]
                    script.append("df.columns = [x[1] if x[1] else x[0] for x in df.columns]")
            else:
                df = df[fields].describe(include=all_, percentiles=all_percentiles)

                script.append(
                    "df = df.describe(include='{}', percentiles={})".format(all_, all_percentiles)
                )

                if pivot_data and len(fields) == 1:
                    df = df.T.reset_index().rename(columns={"index": "column"})
                    script.append("# pivot data")
                    script.append("df = df.T.reset_index().rename(columns={'index': 'column'})")
                else:
                    df = df.reset_index()
                    script.append("df=df.reset_index()")

        except Exception as e:
            msg = "(describe) Exception:" + str(e)
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        df = df.round(2)

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
