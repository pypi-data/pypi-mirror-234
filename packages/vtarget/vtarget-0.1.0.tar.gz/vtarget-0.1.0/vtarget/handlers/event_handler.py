import asyncio
import queue
import threading


class EventHandler:
    def __init__(self):
        self.emit_queue = queue.Queue()
        self.running = True
        self.__event_callback = None

    def on_event(self, callback):
        self.__event_callback = callback

    def event_callback(self, payload):
        if self.__event_callback is not None:
            self.__event_callback(payload)

    def run(self):
        print("Iniciando hilo envio de eventos")
        while self.running:
            payload = self.emit_queue.get(True)
            self.event_callback(payload)

    def init(self):
        asyncio.run(self.run())


event_handler = EventHandler()
worker = threading.Thread(target=event_handler.init)
worker.daemon = True
worker.start()
