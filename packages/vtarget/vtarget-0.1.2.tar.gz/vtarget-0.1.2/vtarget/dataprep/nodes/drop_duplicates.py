import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class DropDuplicates:
    def exec(self, flow_id, node_key, pin, settings):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Drop Duplicates")

        # columns, keep, only_subset

        columns: list[str] = (
            settings["columns"] if ("columns" in settings and settings["columns"] is not []) else []
        )
        keep: str = (
            settings["keep"] if ("keep" in settings and settings["keep"] is not None) else "first"
        )
        only_subset: bool = (
            settings["only_subset"]
            if ("only_subset" in settings and settings["only_subset"] is not None)
            else False
        )

        try:
            if len(columns) == 0:
                df = df.drop_duplicates(keep=keep)
                script.append(f"df = df.drop_duplicates(keep={keep})")
            else:
                df = df.drop_duplicates(subset=columns, keep=keep)
                script.append(f"df = df.drop_duplicates(subset={columns}, keep={keep})")

            if only_subset:
                df = df[columns]
                script.append(f"df = df[{columns}]")

        except Exception as e:
            msg = "(drop_duplicates) Exception:" + str(e)
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

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
