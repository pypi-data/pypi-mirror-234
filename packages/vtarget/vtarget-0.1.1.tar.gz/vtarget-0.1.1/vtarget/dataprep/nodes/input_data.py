import json
import os

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class InputData:
    def exec(self, flow_id, node_key, pin, settings):
        script = []
        # print(node_key)
        encoding: str = (
            settings["encoding"]
            if ("encoding" in settings and settings["encoding"] is not None)
            else "ISO-8859-1"
        )
        dtype = str if "as_string" in settings and settings["as_string"] == True else None
        delimiter: str = (
            settings["delimiter"]
            if "delimiter" in settings and settings["delimiter"] is not None
            else None
        )
        header: str = (
            None if "has_header" in settings and settings["has_header"] == False else "infer"
        )
        # print(encoding)
        # df = pd.read_csv(settings['file_path'], dtype=dtype, encoding=settings['encoding'])

        filename, file_ext = os.path.splitext(settings["file_path"])
        file_ext = file_ext[1:]
        print(filename, file_ext)
        try:
            bug_handler.console(
                'Leyendo fuente "{}"...'.format(settings["file_path"]), "trace", flow_id
            )
            if file_ext in ["csv", "txt"]:
                df = pd.read_csv(
                    settings["file_path"],
                    dtype=dtype,
                    encoding=encoding,
                    delimiter=delimiter,
                    header=header,
                    prefix="col_" if header is None else None,
                )
            elif file_ext == "json":
                orient = settings["orient"] if "orient" in settings else "columns"
                df = pd.read_json(settings["file_path"], orient=orient, encoding=encoding)
            elif file_ext in ["xls", "xlsx", "xlsm", "xlsb"]:
                sheet_name = settings["sheet_name"] if "sheet_name" in settings else 0
                df = pd.read_excel(settings["file_path"], dtype=dtype, sheet_name=sheet_name)
                print(sheet_name)
            else:
                msg = f"(input): Formato {file_ext} no reconocido"
                bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

            df.columns = [str(c) for c in df.columns]

            # revisar si alguna nombre de columna tiene espacio al inicio o al final
            if True in [c.startswith((" ", "\t")) or c.endswith((" ", "\t")) for c in df.columns]:
                df.columns = [c.strip() for c in df.columns]
                msg = f"(input): Archivo fuente contiene espacios al inicio o final del nombre de una o más columnas. Se ha corregido para la lectura"
                bug_handler.default_on_error(
                    flow_id, node_key, msg, console_level="warn", bug_level="warning"
                )

        except Exception as e:
            msg = "(input) Exception:" + str(e)
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        # TODO: Modificar por tipo de archivo, csv, json, excel
        script.append("\n# INPUT")
        script.append(
            "df = pd.read_csv('{}', encoding='{}')".format(settings["file_path"], encoding)
        )
        script.append(f"df = df.astype(str)")
        # script.append(f"df_{node_key}_Out = df_{node_key}_Out.astype(str)")

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
