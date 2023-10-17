import json

import numpy as np
import pandas as pd
from vtarget.handlers.cache_handler import cache_handler


class Utilities:
    # retorna la metadata del dtypes de un df
    def get_dtypes_of_df(self, df: pd.DataFrame):
        dict_dtypes = {}
        res = df.dtypes.to_frame("dtypes")
        # print(res)
        res = res["dtypes"].astype(str).reset_index()
        res["selected"] = True
        res["order"] = pd.RangeIndex(stop=res.shape[0])
        # return res.values.tolist()
        # print(res.columns)
        for _, x in res.iterrows():
            dict_dtypes[x["index"]] = {
                "dtype": x["dtypes"],
                "selected": x["selected"],
                "order": x["order"],
            }

        return dict_dtypes
    
    def get_table_config(self, meta: dict, port_name: str, flow_id: str, node_key: str):
        # # # agregar ports_config a caché
        # # if "ports_config" in meta:
        # #     cache_handler.update_node(flow_id, node_key, { "ports_config": json.dumps(meta["ports_config"], sort_keys=True)})
            
        #? sacar config desde meta.ports_config con el puerto
        ports_config : dict = meta["ports_config"][port_name] if "ports_config" in meta and port_name in meta["ports_config"] else {}
        return {
            "rows": 50 if "rows" not in ports_config else ports_config["rows"],
            "decimals": -1 if "decimals" not in ports_config else ports_config["decimals"],
            "source": "head" if "source" not in ports_config else ports_config["source"],
            "sort_by": [] if "sort_by" not in ports_config else ports_config["sort_by"],
        }

    def sort_df(self, full_df: pd.DataFrame, sorts: list[dict]):
        if sorts:
            setting_list = list(map(lambda x: (x["field"], int(x["ascending"])), [item for item in sorts if "field" in item and item["field"]]))
            if setting_list:
                columns, order = zip(*setting_list)
                if columns and order:
                    full_df = full_df.sort_values(by=list(columns), ascending=list(order))
        return full_df
        
    def get_head_of_df_as_list(self, port_df: pd.DataFrame, config: dict, flow_id: str = None, node_key: str = None, port_name: str = None):
        df: pd.DataFrame = port_df.head(50).copy()
        rows = len(port_df) if config["rows"] > len(port_df) else config["rows"]
        
        # sort
        if "sort_by" in config and len(config["sort_by"]) > 0:
            port_df = self.sort_df(port_df, config["sort_by"])
            cached_node = cache_handler.get_node(flow_id, node_key)
            # actualizar cache del nodo con el nuevo order
            if flow_id and node_key and port_name:
                # actualizar cache del nodo con el nuevo order
                if cached_node["pout"]:
                    cached_node["pout"][port_name] = port_df
                    cache_handler.update_node(flow_id, node_key, { "pout": cached_node["pout"] })
                    
                # cached_node = cache_handler.get_node(flow_id, node_key)
                # if cached_node["pout"]:
                #     pout: dict = dict(cached_node["pout"]).update({ port_name: full_df })
                #     cache_handler.update_node(
                #         flow_id,
                #         node_key,
                #         { "pout": pout },
                #     )
        
        if config["source"] == "head":
            df = port_df[:rows].copy()
        elif config["source"] == "tail":
            df = port_df[-rows:].copy()
        elif config["source"] == "sample":
            df = port_df.sample(rows).copy()
            if "sort_by" in config and len(config["sort_by"]) > 0:
                df = self.sort_df(df, config["sort_by"])
        else:
            df = port_df.head(50).copy()
            print(
                "Source {} no reconocido opciones válidas [head|sample|tail]. Se utilizará head(50)".format(
                    config["source"]
                )
            )
            
        # decimals
        if config["decimals"] != -1:
            df = df.round(config["decimals"])
            
        # Esto para efectos de la visualización al transformar a json
        # special_cols = df.select_dtypes(include=['bool', 'datetime64', 'category']).columns.values.tolist()
        special_cols = df.select_dtypes(
            exclude=[
                "object",
                "int8",
                "int16",
                "int32",
                "int64",
                "float16",
                "float32",
                "float64",
            ]
        ).columns.values.tolist()
        
        if len(special_cols):
            # print(special_cols)
            df[special_cols] = df[special_cols].astype(str)
            
        df = df.fillna("NaN")
        # df = df.replace([np.inf, -np.inf], 0, inplace=True)
        # print(bool_cols)
        # df_head = [df.columns.values.tolist()] + df.values.tolist()
        df_head = df.to_dict("records")
        return df_head

    def format_setting(self, settings, ignore_keys=["ports_map", "readed_from_cache"]):
        setting_copy = {key: value for key, value in settings.items() if key not in ignore_keys}
        return json.dumps(setting_copy, sort_keys=True)

    def viz_summary(self, df):
        cat_col = df.select_dtypes(
            include=["object", "category", "bool", "datetime64", "timedelta"]
        ).columns.tolist()
        num_col = df.select_dtypes(
            include=["int16", "int32", "int64", "float16", "float32", "float64"]
        ).columns.tolist()
        # date_col = df.select_dtypes(include=['datetime64', 'timedelta']).columns.tolist()
        out = {}
        for c in num_col:
            count, bin_ = np.histogram(df[c][np.isfinite(df[c])])
            out[c] = {
                "viz_type": "histogram",
                "y": count.tolist(),
                "x": np.around(bin_, decimals=2).tolist(),
            }

        max_cat = 3
        for c in cat_col:
            cat_viz = "pie"
            vc = df[c].value_counts().iloc[:max_cat]
            vc.index = vc.index.astype("str")
            cat_counts = vc.to_dict()
            if df[c].nunique() > max_cat:
                others = df[~df[c].isin(vc.index)][c].value_counts()
                cat_counts[f"Other ({len(others)})"] = others.sum().item()
                cat_viz = "list"
            out[c] = {"viz_type": cat_viz, "values": cat_counts}
        return out

    def get_central_tendency_measures(self, df):
        if df.empty:
            return {}
        info = df.describe(include="all", datetime_is_numeric=True).T.reset_index()
        # info = info.astype(str)
        # print(info.dtypes)
        jsonlist = json.loads(info.to_json(orient="records"))
        return dict([(x["index"], x) for x in jsonlist])


utilities = Utilities()
