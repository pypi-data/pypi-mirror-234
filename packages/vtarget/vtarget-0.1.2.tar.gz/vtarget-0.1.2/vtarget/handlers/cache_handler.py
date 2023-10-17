import gc
from typing import Dict


class Cache_Handler:
    # class Cache_Handler(threading.Thread):
    cache: Dict[str, Dict]

    def __init__(self):
        # super().__init__()
        self.cache = dict()
        # self.daemon = True
        # self.queue = queue.Queue()
        # self.start()

    def reset(self, flow_id: str):
        if flow_id in self.cache:
            self.cache[flow_id].clear()
            del self.cache[flow_id]
            gc.collect()

    def get_node(self, flow_id: str, node_key: str) -> dict:
        if flow_id in self.cache:
            if node_key in self.cache[flow_id]:
                return self.cache[flow_id][node_key]
        return {}

    def update_node(self, flow_id: str, node_key: str, new_props: dict = {}):
        if flow_id in self.cache:
            if node_key not in self.cache[flow_id]:
                self.cache[flow_id][node_key] = dict()

            self.cache[flow_id][node_key].update(new_props)

    def delete_node(self, flow_id: str, node_key: str) -> bool:
        if flow_id in self.cache:
            if node_key in self.cache[flow_id]:
                del self.cache[flow_id][node_key]
                return True
        return False

    # def dump(self, flow_id: str, node_key: str) -> None:
    #     self.queue.put_nowait(
    #         (
    #             flow_id,
    #             node_key,
    #         )
    #     )

    # def run(self) -> None:
    #     while True:
    #         flow_id, node_key = self.queue.get()
    #         self.__dump(flow_id, node_key)

    # def load(self, flow_id: str, node_key: str) -> None:
    #     if flow_id in self.cache and node_key not in self.cache[flow_id]:
    #         if (
    #             os.path.exists("cache")
    #             and os.path.exists(f"cache/{flow_id}")
    #             and os.path.exists(f"cache/{flow_id}/{node_key}")
    #         ):
    #             try:
    #                 with open(f"cache/{flow_id}/{node_key}", "rb") as file:
    #                     self.cache[flow_id][node_key] = pickle.load(file)
    #             except:
    #                 traceback.print_exception(*sys.exc_info())

    # def __dump(self, flow_id: str, node_key: str) -> None:
    #     if flow_id in self.cache:
    #         try:
    #             if not os.path.exists("cache"):
    #                 os.mkdir("cache")
    #             if not os.path.exists(f"cache/{flow_id}"):
    #                 os.mkdir(f"cache/{flow_id}")
    #             with open(f"cache/{flow_id}/{node_key}", "wb") as file:
    #                 pickle.dump(self.cache[flow_id], file)
    #         except:
    #             import sys
    #             import traceback

    #             traceback.print_exception(*sys.exc_info())

    # def free(self, flow_id: str, node_key: str) -> None:
    #     if flow_id in self.cache and node_key in self.cache[flow_id]:
    #         self.cache[flow_id][node_key].clear()
    #         del self.cache[flow_id][node_key]
    #         gc.collect()


cache_handler = Cache_Handler()
