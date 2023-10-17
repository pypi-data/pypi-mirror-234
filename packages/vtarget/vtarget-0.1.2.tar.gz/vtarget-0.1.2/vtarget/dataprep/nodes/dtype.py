import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.utils.utilities import utilities


class Dtype:
    def __init__(self):
        self.script = []
        # self.sufix_in = ''

    def exec(self, flow_id: str, node_key: str, pin: dict, settings: dict):
        # self.sufix_in = settings['port_In']

        df: pd.DataFrame = pin["In"].copy()
        self.script.append("\n# DTYPE")

        df, _, rename_cols = self.select_types_and_fields(flow_id, node_key, df, settings["items"])

        # Si hay alguna columna para renombrar en las seleccionadas
        if rename_cols:
            try:
                df = df.rename(columns=rename_cols)
            except Exception as e:
                msg = "(dtype) Error al renombrar Exception:" + str(e)
                return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

            self.script.append("\n# RENAME")
            self.script.append("df = df.rename(columns={})".format(rename_cols))

        # if node_key not in cache_handler.cache[flow_id]:
        #     cache_handler.cache[flow_id][node_key] = dict()
        # cache_handler.cache[flow_id][node_key]["pout"] = {"Out": df}
        # cache_handler.cache[flow_id][node_key]["config"] = json.dumps(settings, sort_keys=True)
        # cache_handler.cache[flow_id][node_key]["script"] = self.script
        cache_handler.update_node(
            flow_id, 
            node_key, 
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": self.script,
            }
        )
        
        bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache', "info", flow_id)
        script_handler.script += self.script.copy()
        self.script = []
        # return df, {'dtypes': dtypes}
        # print(df.dtypes)
        return {"Out": df}  # , {'dtypes': dtypes}

    # Retorna el df con las columnas seleccionadas y el tipo de dato
    def select_types_and_fields(self, flow_id: str, node_key: str, df: pd.DataFrame, dtypes: dict):
        # https://pbpython.com/pandas_dtypes.html

        # print('-----> dtypes: ', dtypes)
        # obtengo solo los campos seleccionados de la lista total de campos (selected==True)
        
        # ? para nodos de tipo DTYPE usar todos los campos, sin importar si estan o no en la config
        if 'dtype' in node_key.lower(): #aas
            all_dtypes = utilities.get_dtypes_of_df(df) # ? todos los dtypes del Dataframe
            dtypes = all_dtypes | dtypes
            
        
        selected_dtypes = dict(
            filter(
                lambda x: True if "selected" in x[1] and x[1]["selected"] else False,
                dtypes.items(),
            )) if 'select' in node_key.lower() else dtypes
        
        # selected = dtypes.copy()
        # print("-----> selected:", selected)
        # print("-----> length:", len(selected.items()), len(dtypes.items()))

        # Se maneja la posibilidad de que ya no existan columnas que previamente fueron creadas
        available_cols = []
        removed_cols = []
        for field, x in selected_dtypes.items():
            if field in df.columns:
                available_cols.append(field)
            else:
                removed_cols.append(field)
                del dtypes[field]  # dado que no existe la eliminamos de dtypes
                msg = "(dtype) columa {} no existe en el df".format(field)
                bug_handler.default_on_error(
                    flow_id, node_key, msg, console_level="warn", bug_level="warning", success=True
                )

        # Remuevo las columnas que ya no existen
        for del_key in removed_cols:
            del selected_dtypes[del_key]

        # mantiene solamente columnas existentes y seleccionadas
        df = df[available_cols]
        # print('-----> available_cols:', available_cols)
        # print('-----> df.columns:', df.columns)
        # print('-----> dtypes: ', dtypes)

        self.script.append("df = df[{}]".format(available_cols))
        self.script.append("\n# DATA TYPES")

        rename_cols = {}
        for field, x in selected_dtypes.items():
            # Genero el diccionario para el renombrado de variables
            if "rename" in dtypes[field] and dtypes[field]["rename"]:
                rename_cols[field] = dtypes[field]["rename"]

            standard_dtypes = [
                "object",
                "bool",
                "category",
                "int8",
                "int16",
                "int32",
                "int64",
                "float16",
                "float32",
                "float64",
            ]
            if x["dtype"] in standard_dtypes:
                # si el campo ya es un numérico conocido no lo cambio
                if df[field].dtype == x["dtype"]:
                    continue
                df, status = self.select_change_col_dtype(
                    flow_id, node_key, df.copy(), field, x["dtype"]
                )
                if not status:  # si hubo un error lo vuelvo a texto
                    dtypes[field]["dtype"] = "object"

            elif x["dtype"] in ["datetime64[ns]"]:
                try:
                    df = df.copy()
                    df[field] = pd.to_datetime(df[field])
                except Exception as e:
                    msg = (
                        "(dtype) No fue posible transformar un el campo {} a {}. Exception:".format(
                            field, x["dtype"], str(e)
                        )
                    )
                    bug_handler.default_on_error(flow_id, node_key, msg, str(e))
                    # si hubo un error lo vuelvo a texto
                    dtypes[field]["dtype"] = "object"

            elif x["dtype"] in ["timedelta64[ns]"]:
                try:
                    df = df.copy()
                    df[field] = pd.to_timedelta(df[field])
                except Exception as e:
                    msg = (
                        "(dtype) No fue posible transformar un el campo {} a {}. Exception:".format(
                            field, x["dtype"], str(e)
                        )
                    )
                    bug_handler.default_on_error(flow_id, node_key, msg, str(e))
                    # si hubo un error lo vuelvo a texto
                    dtypes[field]["dtype"] = "object"
            else:
                msg = '(dtype) Tipo de dato "{}" desconocido, campo "{}" se mantiene como string '.format(
                    x["dtype"], field
                )
                bug_handler.default_on_error(
                    flow_id, node_key, msg, console_level="warn", bug_level="warning"
                )
                dtypes[field]["dtype"] = "object"

        # print(df.dtypes)
        # print(dtypes)
        # print(rename_cols)
        # print(' --------------- \n\n ')
        # Ordeno las columnas segun el orden que se le dio en la interfaz
        order_cols = list(dict(sorted(selected_dtypes.items(), key=lambda item: item[1]["order"])).keys())
        return df[order_cols], dtypes, rename_cols

    # Cambia el tipo de dato y maneja los errores que podrían salir en el intento
    def select_change_col_dtype(self, flow_id, node_key, df, field, dtype):
        try:
            # df = df.fillna('')
            df[field] = df[field].astype(dtype)
            # df.loc[:, [field]] = df[field].astype(dtype)
        except Exception as e:
            msg = "(dtype) No fue posible transformar un tipo de dato. Exception:" + str(e)
            bug_handler.default_on_error(flow_id, node_key, msg, str(e))
            return df, False
        else:
            dtype_ = dtype if isinstance(dtype, str) else dtype.__name__
            self.script.append("df['{0}'] = df['{0}'].astype('{1}')".format(field, dtype_))
            return df, True
