import json

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Column:
    def __init__(self):
        self.script = []
        # self.sufix_in = ''

    def exec(self, flow_id, node_key, pin, settings):
        # self.sufix_in = settings['port_In']

        df = pin["In"].copy()
        self.script.append("\n# COLUMN")

        df, _, rename_cols = self.select_types_and_fields(flow_id, node_key, df, settings["items"])

        # Si hay alguna columna para renombrar en las seleccionadas
        if rename_cols:
            try:
                df = df.rename(columns=rename_cols)
            except Exception as e:
                msg = "(column) Error al renombrar, exception:" + str(e)
                return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

            self.script.append("\n# RENAME")
            self.script.append("df = df.rename(columns={})".format(rename_cols))

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": self.script,
            },
        )

        bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache', "info", flow_id)
        script_handler.script += self.script.copy()
        self.script = []
        # return df, {'dtypes': dtypes}
        # print(df.dtypes)
        return {"Out": df}  # , {'dtypes': dtypes}

    # Retorna el df con las columnas seleccionadas y el tipo de dato
    def select_types_and_fields(self, flow_id, node_key, df, dtypes):
        # https://pbpython.com/pandas_dtypes.html

        # print('-----> dtypes: ', dtypes)
        # obtengo solo los campos seleccionados de la lista total de campos (selected==True)
        selected = dict(
            filter(
                lambda x: True if "selected" in x[1] and x[1]["selected"] else False,
                dtypes.items(),
            )
        )
        # print('-----> selected:', selected)

        # Se maneja la posibilidad de que ya no existan columnas que previamente fueron creadas
        available_cols = []
        removed_cols = []
        for field, _ in selected.items():
            if field in df.columns:
                available_cols.append(field)
            else:
                removed_cols.append(field)
                del dtypes[field]  # dado que no existe la eliminamos de dtypes
                msg = "(column) columa {} no existe en el df".format(field)
                bug_handler.default_on_error(
                    flow_id, node_key, msg, console_level="warn", bug_level="warning", success=True
                )

        # Remuevo las columnas que ya no existen
        for del_key in removed_cols:
            del selected[del_key]

        # mantiene solamente columnas existentes y seleccionadas
        df = df[available_cols]
        # print('-----> available_cols:', available_cols)
        # print('-----> df.columns:', df.columns)
        # print('-----> dtypes: ', dtypes)

        self.script.append("df = df[{}]".format(available_cols))
        self.script.append("\n# DATA TYPES")

        rename_cols = {}
        for field, _ in selected.items():
            # Genero el diccionario para el renombrado de variables
            if "rename" in dtypes[field] and dtypes[field]["rename"]:
                rename_cols[field] = dtypes[field]["rename"]

        # Ordeno las columnas segun el orden que se le dio en la interfaz
        order_cols = list(dict(sorted(selected.items(), key=lambda item: item[1]["order"])).keys())
        return df[order_cols], dtypes, rename_cols

    # Cambia el tipo de dato y maneja los errores que podrían salir en el intento
    def select_change_col_dtype(self, flow_id, node_key, df, field, dtype):
        try:
            # df = df.fillna('')
            df[field] = df[field].astype(dtype)
            # df.loc[:, [field]] = df[field].astype(dtype)
        except Exception as e:
            msg = "(column) No fue posible transformar un tipo de dato. Exception:" + str(e)
            bug_handler.default_on_error(flow_id, node_key, msg, str(e))
            return df, False
        else:
            dtype_ = dtype if isinstance(dtype, str) else dtype.__name__
            self.script.append("df['{0}'] = df['{0}'].astype('{1}')".format(field, dtype_))
            return df, True
