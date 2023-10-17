import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler


class VOutput:
    def exec(self, flow_id, node_key, pin, settings):
        df: pd.DataFrame = pin["In"].copy()

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": [],
                "type": "V_Output",
            },
        )

        bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache', "info", flow_id)
        # script_handler.script += script

        return pd.DataFrame()
