import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Groupby:
    def exec(self, flow_id, node_key, pin, settings):
        script = []

        # if node_key in cache_handler.cache[flow_id] and cache_handler.cache[flow_id][node_key]['config'] == json.dumps(settings, sort_keys=True):
        # 	bug_handler.console(f'Nodo "{node_key}" leído desde cache flow_id: "{flow_id}"', 'info')
        # 	reset_childs = False
        # 	script_handler.script += cache_handler.cache[flow_id][node_key]['script']
        # 	return cache_handler.cache[flow_id][node_key]['pout'], reset_childs

        df = pin["In"].copy()
        # print('\n\n\n node_key: ', node_key, '\n\n\n')
        script.append("\n# GROUPBY")

        def percentile(n):
            def percentile_(x):
                return np.percentile(x, n)

            percentile_.__name__ = "q%s" % n
            return percentile_

        def count_distinct(x):
            return x.nunique()

        # count_distinct = lambda x: x.nunique()

        def count_null(x):
            return x.isnull().sum()

        def mode(x):
            # return x.value_counts().index[0]
            return x.value_counts().idxmax()

        def count_blank(x):
            return sum(x == "")

        def count_not_blank(x):
            return sum(x == "")

        # https://www.analyticsvidhya.com/blog/2020/03/groupby-pandas-aggregating-data-python/
        group_by_cols = settings["group_by"] if "group_by" in settings else []
        agg_cols = {}
        # pctl_dynamic = {}
        # pctl_replaces = []
        pctl_replaces2 = []
        rename_cols = {}
        # group_by_rename = {}

        # print(settings['group_by'])
        # print(settings['agg'])

        for a in settings["agg"]:
            # if a['action'] == 'group_by': # obtengo las columnas del groupby
            # 	group_by_cols.append(a['column'])
            # 	if 'rename' in a and a['rename']: # agrego los rename asociado a la columna de agrupación
            # 		rename_cols[a['column']] = a['rename']
            # else:
            action = a["action"]
            if action == "percentile":
                # print('----------------------------------------------------')
                # print(action, a['pctl_value'])
                fn_name = "quantile_{}".format(a["pctl_value"])
                # user_fn_name = 'p{}_{}'.format(a['pctl_value'], a['column'])
                # print(int(a['pctl_value'])/100)
                # pctl_dynamic[fn_name] = lambda x :  x.quantile(q=int(a['pctl_value'])/100)
                # pctl_dynamic[fn_name].__name__ = 'p{}'.format(a['pctl_value'])
                # exec('{} = lambda x :  x.quantile(q={})'.format(fn_name, int(a['pctl_value'])/100))
                # # locals()[fn_name] = lambda x :  x.quantile(q=int(a['pctl_value'])/100)
                # exec('{}.__name__ = "{}"'.format(fn_name, user_fn_name))
                # exec("a['action'] = quantile_{}".format(a['pctl_value']))
                # a['action'] = pctl_dynamic[fn_name]
                action = fn_name
                # pctl_replaces.append(fn_name)
                pctl_replaces2.append((fn_name, a["pctl_value"]))

            # luego agrupo las funciones de agregación
            if a["column"] not in agg_cols:
                agg_cols[a["column"]] = [action]
            else:
                # valido que no se agreguen agregaciones repetidas
                if action not in agg_cols[a["column"]]:
                    agg_cols[a["column"]].append(action)
            # Si viene una columna de agregación con un renombre desde la vista
            if "rename" in a and a["rename"]:
                # print(a['column'], '->', a['rename'])
                # creo el nombre compuesto entre la columna y la fn de agg
                current_name = a["column"] + "_" + action
                rename_cols[current_name] = a["rename"]
        # print(pctl_dynamic)
        agg_str = str(agg_cols)
        # for pr in pctl_replaces:
        for pr in pctl_replaces2:
            # agg_str = agg_str.replace("'{}'".format(pr), "pctl_dynamic['{}']".format(pr))
            agg_str = agg_str.replace("'{}'".format(pr[0]), "percentile({})".format(pr[1]))
        if "count_distinct" in agg_str:
            agg_str = agg_str.replace("'count_distinct'", "count_distinct")
        if "count_null" in agg_str:
            agg_str = agg_str.replace("'count_null'", "count_null")
        if "mode" in agg_str:
            agg_str = agg_str.replace("'mode'", "mode")

        # print('\n -------------------------------------------')
        # print(df)
        # # print(settings)
        # print('group_by_cols:', group_by_cols) # group_by_cols: ['segmento_1']
        # print('agg_cols: ', agg_cols) # agg_cols:  {'rut': ['count_distinct']}
        # print('agg_str: ', agg_str) # agg_str:  {'rut': [count_distinct]}
        # print('rename_cols: ', rename_cols) #
        # print('\n -------------------------------------------')

        grouped = pd.DataFrame()
        try:
            if group_by_cols:
                # print('df.groupby(group_by_cols).agg({}).reset_index()'.format(agg_str))
                # exec('grouped = df.groupby(group_by_cols).agg({}).reset_index()'.format(agg_str))
                grouped = eval("df.groupby(group_by_cols).agg({}).reset_index()".format(agg_str))
                # print('grouped.columns (raw):', grouped.columns)
                # Dado que las columnas vienen en un multiIndex, con esto reseteo el indice
                grouped.columns = ["_".join(x) if x[1] else x[0] for x in grouped.columns]
                # print('grouped.columns (renamed):', grouped.columns)
                script.append(
                    "grouped = df.groupby({}).agg({}).reset_index()".format(group_by_cols, agg_str)
                )
            else:
                # df = df.copy()
                grouped = eval("df.groupby(lambda _ : 1).agg({}).reset_index()".format(agg_str))
                # print('\n\n')
                # print(grouped.columns)
                # print(list(grouped.columns))
                grouped.columns = ["_".join(x) if x[1] else x[0] for x in grouped.columns]
                grouped.drop(columns=["index"], axis=1, inplace=True)
                script.append(
                    "grouped = df.groupby(lambda _ : 1).agg({}).reset_index()".format(agg_str)
                )
        except Exception as e:
            msg = "(groupby) Exception:" + str(e)
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        try:
            grouped.rename(columns=rename_cols, inplace=True)
        except Exception as e:
            msg = "(groupby) No fue realizar el rename luego de la sumarización. Exception:" + str(
                e
            )
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": grouped},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache', "info", flow_id)
        script_handler.script += script

        return {"Out": grouped}
