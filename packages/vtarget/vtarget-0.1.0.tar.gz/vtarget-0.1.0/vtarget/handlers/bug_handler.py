import pandas as pd
from termcolor import colored

from vtarget.handlers.log_handler import log_handler


class Bug_Handler:
    def __init__(self):
        self.bug = []
        self.__append_handler = None

    def on_append(self, handler):
        self.__append_handler = handler

    def append_handler(self, bug):
        if self.__append_handler is not None:
            self.__append_handler(bug)

    def append(self, bug, use_handler=True):
        self.bug.append(bug)
        if use_handler:
            # await socket_server.emit('dataprep.bug', bug) # TODO: Mover a py
            self.append_handler(bug)

    def console(self, msg, level, flow_id, emit=True):
        level = level.upper()
        if level == "DEBUG":
            color = "green"
        elif level == "INFO":
            color = "cyan"
        elif level == "WARN":
            color = "yellow"
        elif level == "ERROR":
            color = "red"
        elif level == "FATAL":
            color = "white"
            print(colored(f"[{level}] {msg}", color, "on_red"))
            return
        elif level == "TRACE":
            color = "magenta"
        else:
            color = "white"
        print(colored(f"[{level}] {msg}", color))
        log_handler.append({"flow_id": flow_id, "level": level, "msg": msg, "color": color}, emit)

    def default_on_error(
        self,
        flow_id: str,
        node_key: str,
        msg: str,
        exception="",
        console_level="fatal",
        bug_level="error",
        success=False,
    ):
        self.console(msg, console_level, flow_id)
        self.append(
            {
                "flow_id": flow_id,
                "success": success,
                "node_key": node_key,
                "level": bug_level,
                "msg": msg,
                "exception": exception,
            }
        )
        return {"Out": pd.DataFrame()}


bug_handler = Bug_Handler()
