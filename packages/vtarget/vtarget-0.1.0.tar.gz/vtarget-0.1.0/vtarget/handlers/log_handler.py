class Log_Handler:
    def __init__(self):
        self.log = []
        self.__append_handler = None

    def on_append(self, handler):
        self.__append_handler = handler

    def append_handler(self, log):
        if self.__append_handler is not None:
            self.__append_handler(log)

    def append(self, log, use_handler=True):
        self.log.append(log)
        if use_handler:
            self.append_handler(log)


log_handler = Log_Handler()
