import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Merge:
    def __init__(self):
        self.script = []

    def exec(self, flow_id, node_key, pin, settings):
        # if node_key in cache_handler.cache[flow_id] and cache_handler.cache[flow_id][node_key]['config'] == json.dumps(settings, sort_keys=True):
        # 	bug_handler.console(f'Nodo "{node_key}" leído desde cache flow_id: "{flow_id}"', 'info', flow_id)
        # 	reset_childs = False
        # 	script_handler.script += cache_handler.cache[flow_id][node_key]['script']
        # 	return cache_handler.cache[flow_id][node_key]['pout'], reset_childs
        if "iL" not in pin or "iR" not in pin:
            msg = "(merge) Puerto entrada iL/iR no conectado"
            bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
            edf = pd.DataFrame()
            return {"L": edf, "J": edf, "R": edf, "F": edf}

        self.script.append("\n# MERGE")
        df_iL: pd.DataFrame = pin["iL"][settings["left_columns"]].copy()
        df_iR: pd.DataFrame = pin["iR"][settings["right_columns"]].copy()

        on_l: list[str] = [x["left"] for x in settings["items"] if x["left"]]
        on_r: list[str] = [x["right"] for x in settings["items"] if x["right"]]

        # if len(settings['outputs']) == 4 or 'F' in settings['outputs']: # [L,J,R,F] o si incluye F
        # 	pout_struct = self.full_outer_join(flow_id, node_key, df_iL, df_iR, on_l, on_r)
        # else:
        edf = pd.DataFrame()
        pout_struct = {"L": edf, "J": edf, "R": edf, "F": edf}
        if "L" in settings["outputs"]:
            pout_struct["L"] = self.apply_join(flow_id, node_key, "left", df_iL, df_iR, on_l, on_r)
        if "J" in settings["outputs"]:
            pout_struct["J"] = self.apply_join(flow_id, node_key, "inner", df_iL, df_iR, on_l, on_r)
        if "R" in settings["outputs"]:
            pout_struct["R"] = self.apply_join(flow_id, node_key, "right", df_iL, df_iR, on_l, on_r)
        if "F" in settings["outputs"]:
            pout_struct["F"] = self.apply_join(flow_id, node_key, "outer", df_iL, df_iR, on_l, on_r)

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": pout_struct,
                "config": json.dumps(settings, sort_keys=True),
                "script": self.script,
            },
        )

        bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache', "info", flow_id)
        script_handler.script += self.script
        return pout_struct

    def apply_join(self, flow_id, node_key, how, df_iL, df_iR, on_l, on_r):
        try:
            if how == "outer":
                df_o = pd.merge(
                    df_iL,
                    df_iR,
                    left_on=on_l,
                    right_on=on_r,
                    how="outer",
                    indicator=True,
                )  # , validate="many_to_one")
                # campo _merge viene como category, lo cambio a object (str)
                df_o["merge_type"] = df_o["_merge"].astype(str)
                del df_o["_merge"]
                # df_o["_merge"] = df_o["_merge"].astype(str)
                self.script.append(
                    "df_o = pd.merge(df_iL, df_iR, left_on={}, right_on={}, how='outer', indicator=True)".format(
                        on_l, on_r
                    )
                )
            else:
                # , validate="many_to_one")
                df_o = pd.merge(df_iL, df_iR, left_on=on_l, right_on=on_r, how=how)
                self.script.append(
                    "df_o = pd.merge(df_iL, df_iR, left_on={}, right_on={}, how='{}', indicator=True)".format(
                        on_l, on_r, how
                    )
                )
        except Exception as e:
            msg = "(merge) Exception:" + str(e)
            bug_handler.default_on_error(flow_id, node_key, msg, str(e))
            return pd.DataFrame()
        return df_o

    # def full_outer_join(self, flow_id, node_key, df_iL, df_iR, on_l, on_r):
    # 	try:
    # 		# Outer join con indicator (que genera la columna merge) para sacar sólo las columnas de lado correspondiente
    # 		df_o = pd.merge(df_iL, df_iR, left_on=on_l, right_on=on_r, how="outer", indicator=True)#, validate="many_to_one")
    # 		self.script.append("df_o = pd.merge(df_iL, df_iR, left_on={}, right_on={}, how='outer', indicator=True)".format(on_l, on_r))
    # 	except Exception as e:
    # 		msg = '(merge) Exception:' + str(e)
    # 		bug_handler.console(msg, 'fatal', flow_id)
    # 		bug_handler.append({'flow_id': flow_id, 'success': False, 'node_key': node_key, 'level': 'error', 'msg': msg, 'exception': str(e)})
    # 		edf = pd.DataFrame()
    # 		return {'L': edf, 'J': edf, 'R': edf, 'F': edf}

    # 	# print('J',df_iL.shape, df_iR.shape)
    # 	df_l = df_o[df_o['_merge'].isin(['left_only', 'both'])].drop(columns=['_merge'], axis=1) # where 1 is the axis number (0 for rows and 1 for columns.)
    # 	df_j = df_o[df_o['_merge'] == 'both'].drop(columns=['_merge'], axis=1) # where 1 is the axis number (0 for rows and 1 for columns.)
    # 	df_r = df_o[df_o['_merge'].isin(['right_only', 'both'])].drop(columns=['_merge'], axis=1) # where 1 is the axis number (0 for rows and 1 for columns.)

    # 	self.script.append("df_l = df_o[df_o['_merge'] == 'left_only'].drop(columns=['_merge'], axis=1)")
    # 	self.script.append("df_j = df_o[df_o['_merge'] == 'both'].drop(columns=['_merge'], axis=1)")
    # 	self.script.append("df_r = df_o[df_o['_merge'] == 'right_only'].drop(columns=['_merge'], axis=1)")

    # 	df_o['_merge'] = df_o['_merge'].astype(str) # campo _merge viene como category, lo cambio a object (str)
    # 	# df_o.rename(columns={'_merge': 'merge'}, inplace=True)
    # 	# print(df_j.head())

    # 	return {'L': df_l, 'J': df_j, 'R': df_r, 'F': df_o}
