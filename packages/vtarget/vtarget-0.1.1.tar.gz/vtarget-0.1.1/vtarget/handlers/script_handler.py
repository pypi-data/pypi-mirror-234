class Script_Handler:
    def __init__(self):
        self.script = []

    def reset(self, flow_id):
        self.script[flow_id] = []


script_handler = Script_Handler()
