import json

import numpy as np
import pandas as pd


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

    def get_head_of_df_as_list(self, full_df, config):
        # df = full_df.head(50).copy()
        rows = len(full_df) if config["rows"] > len(full_df) else config["rows"]
        if config["source"] == "head":
            df = full_df[:rows].copy()
        elif config["source"] == "tail":
            df = full_df[-rows:].copy()
        elif config["source"] == "sample":
            df = full_df.sample(rows).copy()
        else:
            df = full_df.head(50).copy()
            print(
                "Source {} no reconocido opciones válidas [head|sample|tail]. Se utilizará head(50)".format(
                    config["source"]
                )
            )
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
