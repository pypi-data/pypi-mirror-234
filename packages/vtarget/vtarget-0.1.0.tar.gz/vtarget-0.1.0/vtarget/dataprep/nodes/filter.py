import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Filter:
    def __init__(self):
        self.script = []
        # self.sufix_in = ''

    def exec(self, flow_id, node_key, pin, settings):
        # self.sufix_in = settings['port_In']

        if "rule_type" not in settings:
            msg = "(filter) No se ha creado ninguna una regla"
            bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
            return {"T": pd.DataFrame(), "F": pd.DataFrame()}

        # if "sensitive_case" in settings and settings["sensitive_case"]:
        #     settings["value"] = settings["value"].lower()

        df: pd.DataFrame = pin["In"].copy()
        df_T, df_F = pd.DataFrame(), pd.DataFrame()
        # print(settings)
        if settings["rule_type"] == "preconfigured":
            try:
                df_T, df_F = self.filter_preconfigured(flow_id, node_key, df, settings)
            except Exception as e:
                msg = "(filter) Exception:" + str(e)
                bug_handler.default_on_error(flow_id, node_key, msg, str(e))
                return {"T": pd.DataFrame(), "F": pd.DataFrame()}

        elif settings["rule_type"] == "code":
            df_T, df_F = self.filter_code(flow_id, node_key, df, settings["sentence"])
        else:
            msg = '(filter_code) No reconoce la regla "{}"'.format(settings["rule_type"])
            bug_handler.default_on_error(
                flow_id, node_key, msg, console_level="warn", bug_level="warning"
            )

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"T": df_T, "F": df_F},
                "config": json.dumps(settings, sort_keys=True),
                "script": self.script,
            },
        )

        bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache', "info", flow_id)
        script_handler.script += self.script.copy()
        self.script = []

        return {"T": df_T, "F": df_F}

    # Nodo: filter - Procesa el filtro de sentencia
    def filter_code(self, flow_id, node_key, df, sentence):
        self.script.append("\n# FILTER (CUSTOMIZED)")
        # self.script.append(f"df = df_{self.sufix_in}")
        str_rule = "df[{}]".format(sentence)
        # print(df.dtypes)
        # print(str_rule)
        try:
            df_T = eval(str_rule)
            # df_T = pd.eval(str_rule)
            self.script.append("df_T = {}".format(str_rule))
        except Exception as e:
            msg = "(filter_code) No fue posible procesar la condición. Exception:" + str(e)
            bug_handler.default_on_error(flow_id, node_key, msg, str(e))
            return pd.DataFrame(), pd.DataFrame()
        else:
            # Obtengo el complemento (la parte negada de la condición)
            df_F = df[~df.index.isin(df_T.index)]
            self.script.append("df_F = df[~df.index.isin(df_T.index)]")
            return df_T, df_F

    # Nodo: filter - Procesa el filtro preconfigurado
    def filter_preconfigured(self, flow_id, node_key, df: pd.DataFrame, rule):
        df_T, df_F = pd.DataFrame(), pd.DataFrame()
        self.script.append("\n# FILTER (PRECONFIGURED)")
        # self.script.append(f"df = df_{self.sufix_in}")
        field: str = rule["field"]
        operator: str = rule["operator"]
        value: str = rule["value"] if "value" in rule else '""'
        sensitive_case: bool = (
            True
            if pd.api.types.is_string_dtype(df[field])
            and "sensitive_case" in rule
            and rule["sensitive_case"]
            else False
        )

        if field not in df.columns:
            msg = "(filter_code) No existe la columna {} en el dataframe de entrada".format(field)
            bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
            return pd.DataFrame(), pd.DataFrame()

        if pd.api.types.is_datetime64_any_dtype(df[field]):
            value = "'{}'".format(value)

        # print( '{} {} {}'.format(field, operator, value) )
        # print(df.dtypes)
        # is_numeric_dtype(df['B'])
        # Lógica para crear los filtros
        if operator == "=":  # Numeric, String
            if pd.api.types.is_string_dtype(df[field]):
                value = "'{}'".format(value)

            str_rule = "df[(df['{}'] == {})]".format(field, value)
            if not sensitive_case:
                str_rule = "df[(df['{}'].str.lower() == {}.lower())]".format(field, value)

            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "!=":  # Numeric, String
            if pd.api.types.is_string_dtype(df[field]):
                value = "'{}'".format(value)

            str_rule = "df[(df['{}'] != {})]".format(field, value)
            if not sensitive_case:
                str_rule = "df[(df['{}'].str.lower() != {}.lower())]".format(field, value)
            # print('\n\n', str_rule, '\n\n')
            # print(df.dtypes)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "<":  # Numeric
            str_rule = "df[(df['{}'] < {})]".format(field, value)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "<=":  # Numeric
            str_rule = "df[(df['{}'] <= {})]".format(field, value)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == ">":  # Numeric
            str_rule = "df[(df['{}'] > {})]".format(field, value)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == ">=":  # Numeric
            str_rule = "df[(df['{}'] >= {})]".format(field, value)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "is_null":  # Numeric, String
            df_T = df[df[field].isnull()]
            self.script.append("df_T = df[df['{}'].isnull()]".format(field))
        elif operator == "is_not_null":  # Numeric, String
            df_T = df[df[field].notnull()]
            self.script.append("df_T = df[df['{}'].notnull()]".format(field))
        elif operator == "contains":  # String
            df_T = df[df[field].str.contains(value, case=sensitive_case)]
            self.script.append(
                "df_T = df[df['{}'].str.contains('{}', case={})]".format(
                    field, value, sensitive_case
                )
            )
        elif operator == "does_not_contain":  # String
            df_T = df[~df[field].str.contains(value, case=sensitive_case)]
            self.script.append(
                "df_T = df[~df['{}'].str.contains('{}', case={})]".format(
                    field, value, sensitive_case
                )
            )
        elif operator == "is_empty":  # String
            str_rule = "df[(df['{}'] == " ")]".format(field)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "is_not_empty":  # String
            str_rule = "df[(df['{}'] != " ")]".format(field)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "is_true":  # True
            str_rule = "df[(df['{}'] == True)]".format(field)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        elif operator == "is_false":  # False
            str_rule = "df[(df['{}'] == False)]".format(field)
            df_T = eval(str_rule)
            self.script.append(f"df_T = {str_rule}")
        else:
            msg = '(filter_code) Operador no reconocido "{}"'.format(rule["operator"])
            bug_handler.default_on_error(
                flow_id, node_key, msg, console_level="error", bug_level="error"
            )

        # Obtengo el complemento (la parte negada de la condición)
        df_F = df[~df.index.isin(df_T.index)]
        self.script.append(f"df_F = df[~df.index.isin(df_T.index)]")
        # print(df.head())
        return df_T, df_F
