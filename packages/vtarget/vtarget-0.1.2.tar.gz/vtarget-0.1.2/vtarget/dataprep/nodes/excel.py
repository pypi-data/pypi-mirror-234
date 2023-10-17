import json
import math

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class ExcelOutput:
    def exec(self, flow_id, node_key, pin, settings):
        script_handler.script.append("\n# EXCEL")
        output_name: str = (
            settings["name"] if "name" in settings and settings["name"] is not None else "output"
        )
        output_path: str = (
            settings["path"] if "path" in settings and settings["path"] is not None else ""
        )
        encoding: str = settings["encoding"] or "UTF-8"

        # print(columns, order)
        df1 = pin["In"].copy() if "In" in pin else pd.DataFrame()
        df2 = pin["In2"].copy() if "In2" in pin else pd.DataFrame()
        df3 = pin["In3"].copy() if "In3" in pin else pd.DataFrame()
        df4 = pin["In4"].copy() if "In4" in pin else pd.DataFrame()
        df5 = pin["In5"].copy() if "In5" in pin else pd.DataFrame()

        sheet_name_1: str = (
            settings["sheet1"]
            if "sheet1" in settings and settings["sheet1"] != ""
            else "sheet_1"
        )
        sheet_name_2: str = (
            settings["sheet2"]
            if "sheet2" in settings and settings["sheet2"] != ""
            else "sheet_2"
        )
        sheet_name_3: str = (
            settings["sheet3"]
            if "sheet3" in settings and settings["sheet3"] != ""
            else "sheet_3"
        )
        sheet_name_4: str = (
            settings["sheet4"]
            if "sheet4" in settings and settings["sheet4"] != ""
            else "sheet_4"
        )
        sheet_name_5: str = (
            settings["sheet5"]
            if "sheet5" in settings and settings["sheet5"] != ""
            else "sheet_5"
        )

        file_path: str = f"{output_path}\\{output_name}.xlsx"
        settings["file_path"] = file_path

        # TODO: Agregar script
        try:
            # create a excel writer object
            with pd.ExcelWriter(file_path) as writer:
                # use to_excel function and specify the sheet_name and index
                # to store the dataframe in specified sheet
                if len(df1) > 0:
                    self.pd_to_excel(df1, writer, sheet_name_1, encoding)
                    # df1.to_excel(writer, sheet_name=sheet_name_1, index=False, encoding=encoding)
                if len(df2) > 0:
                    self.pd_to_excel(df2, writer, sheet_name_2, encoding)
                    # df2.to_excel(writer, sheet_name=sheet_name_2, index=False, encoding=encoding)
                if len(df3) > 0:
                    self.pd_to_excel(df3, writer, sheet_name_3, encoding)
                    # df3.to_excel(writer, sheet_name=sheet_name_3, index=False, encoding=encoding)
                if len(df4) > 0:
                    self.pd_to_excel(df4, writer, sheet_name_4, encoding)
                    # df4.to_excel(writer, sheet_name=sheet_name_4, index=False, encoding=encoding)
                if len(df5) > 0:
                    self.pd_to_excel(df5, writer, sheet_name_5, encoding)
                    # df5.to_excel(writer, sheet_name=sheet_name_5, index=False, encoding=encoding)

        except Exception as e:
            msg = f"(excel) No fue posible generar el archivo excel: {str(e)}"
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        out = []
        sheet_names = [sheet_name_1, sheet_name_2, sheet_name_3, sheet_name_4, sheet_name_5]
        for idx, df in enumerate([df1, df2, df3, df4, df5]):
            if len(df):
                out.append(
                    {
                        "Name": sheet_names[idx],
                        "Columns": len(df.columns),
                        "Rows": len(df),
                        # "File_Path": file_path,
                    }
                )

        df = pd.DataFrame(out)

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script_handler.script,
            },
        )

        bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache', "info", flow_id)
        return {"Out": df}

    def pd_to_excel(self, df: pd.DataFrame, writer: pd.ExcelWriter, sheet_name: str, encoding: str):
        # https://support.microsoft.com/en-us/office/excel-specifications-and-limits-1672b34d-7043-467e-8e27-269d656771c3?ui=en-us&rs=en-us&ad=us
        rows: int = len(df)
        rows_per_sheet = 1048576 - 1  # max rows by worksheet = 1048576
        if rows > rows_per_sheet:
            steps = math.ceil(rows / rows_per_sheet)
            start = 0
            end = rows_per_sheet
            for idx in range(steps):
                step_df = df.copy().iloc[start:end]
                step_df.to_excel(
                    writer, sheet_name=f"{sheet_name}_{idx + 1}", index=False, encoding=encoding
                )
                start = end
                end += rows_per_sheet
        else:
            df.to_excel(writer, sheet_name=sheet_name, index=False, encoding=encoding)
