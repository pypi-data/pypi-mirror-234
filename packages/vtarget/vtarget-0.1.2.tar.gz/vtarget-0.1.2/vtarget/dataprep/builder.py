import gc
import json
import time

import pandas as pd

from vtarget.dataprep.pipeline import Pipeline
from vtarget.dataprep.types import NodeType
from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.event_handler import event_handler
from vtarget.handlers.log_handler import log_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.utils.utilities import utilities


class Builder:
    def __init__(self):
        # self.compute_node_counter = 0
        self.nodes: dict = {}
        self.script: str = ""
        self.init_script()  # resetea el script
        self.cur_node_key: str = None
        # self.ultra = None

    def init_pipeline(self):
        self.pipeline = Pipeline()

    def init_script(self):
        # Headers del script
        script_handler.script.append("#!/usr/bin/env python")
        script_handler.script.append("# coding: utf-8\n")
        script_handler.script.append("import pandas as pd")
        script_handler.script.append("import numpy as np")

    def set_nodes(self, flow_id: str, data: dict):
        # node_data = {}
        self.nodes = (
            {}
        )  # diccionario con los nodos del flujo cuya clave es el atributo "key" del nodo
        for idx, nd in enumerate(data["nodeDataArray"]):
            if (
                not ("isGroup" in nd and nd["isGroup"])  # no es grupo
                and (nd["type"] not in ["Comment"])  # no es comment
                and (nd["category"] not in ["chart"])  # no es chart
            ):
                self.nodes[nd["key"]] = {
                    "idx": idx,
                    "name": nd["name"],
                    "type": nd["type"],
                    "key": nd["key"],
                    "loaded": False,
                    "output": None,
                    "parents": [],
                    "childs": [],
                    # "is_group": "isGroup" in nd and nd["isGroup"],
                    "skip": False,
                }

        # recorrer los links para obtener los padres e hijos por nodo
        for ld in data["linkDataArray"]:
            if "_chart" in ld["to"]:
                continue
            # Agrego los padres
            parent = {"from": ld["from"], "frompid": ld["frompid"], "topid": ld["topid"]}
            if not self.nodes[ld["to"]]["parents"]:
                self.nodes[ld["to"]]["parents"] = [parent]
            else:
                self.nodes[ld["to"]]["parents"].append(parent)

            # Agrego los hijos
            child = {
                "to": ld["to"],
                "topid": ld["topid"],
                "frompid": ld["frompid"],
                "to_id": self.nodes[ld["to"]]["idx"],
            }
            if not self.nodes[ld["from"]]["childs"]:
                self.nodes[ld["from"]]["childs"] = [child]
            else:
                self.nodes[ld["from"]]["childs"].append(child)

        # print(self.node_data)
        # print('Tamaño inicial self.node_data (bytes): ',sys.getsizeof(self.node_data))

    # Resetea todos los nodos hijos cuando cambia la configuración de un padre
    def reset_childs_recursive(self, flow_id: str, node_key: str, reseted_nodes: list):
        for child in self.nodes[node_key]["childs"]:
            if child["to"] in cache_handler.cache[flow_id]:
                del cache_handler.cache[flow_id][child["to"]]
                # print('-----------------> caché reseteada para nodo',childs['to'])
                reseted_nodes.append(child["to"])
            self.reset_childs_recursive(flow_id, child["to"], reseted_nodes)
        return reseted_nodes

    # Setea a True el parámetro para saltar (no-procesar) los nodos hijos cuando existe un error
    def set_skip_childs_recursive(self, flow_id: str, node_key: str, data: dict):
        for child in self.nodes[node_key]["childs"]:
            # habilita la bandera para saltarse el nodo
            self.nodes[child["to"]]["skip"] = True
            # resetea el df completo almacenado en RAM
            self.nodes[child["to"]]["output"] = None
            # resetea el nodo de gojs
            # data['nodeDataArray'][childs['to_id']]['meta']['ports_map']['pout'] = {}
            for pout_name in data["nodeDataArray"][child["to_id"]]["meta"]["ports_map"]["pout"]:
                data["nodeDataArray"][child["to_id"]]["meta"]["ports_map"]["pout"][pout_name][
                    "head"
                ] = []
                data["nodeDataArray"][child["to_id"]]["meta"]["ports_map"]["pout"][pout_name][
                    "rows"
                ] = 0
                data["nodeDataArray"][child["to_id"]]["meta"]["ports_map"]["pout"][pout_name][
                    "cols"
                ] = 0
                # data['nodeDataArray'][childs['to_id']]['meta']['ports_map']['pout'][pout_name]['dtypes'] = None
            data["nodeDataArray"][child["to_id"]]["meta"]["skipped"] = True
            print("=================> se saltará el nodo", child["to"])
            self.set_skip_childs_recursive(flow_id, child["to"], data)
        return True

    def analyzer(
        self,
        data: dict,
        reset_cache: bool,
        flow_id: str,
        flow_name: str,
        disable_all_write_nodes: bool,
        decimal_round,
    ):
        # Reseteo de variables singleton para cada ejecución
        log_handler.log = []
        bug_handler.bug = []
        script_handler.script = []
        self.pipeline.decimal_round = decimal_round

        # Si se corre el flujo reseteando la cache
        if reset_cache:
            msg = f'Caché reseteada para el flujo "{flow_name}"'
            bug_handler.default_on_error(
                flow_id, None, msg, console_level="trace", bug_level="info", success=True
            )
            cache_handler.reset(flow_id)

        # Incializa la caché para el nodo si es que aún no existe
        if flow_id not in cache_handler.cache:
            cache_handler.cache[flow_id] = dict()

        cache_nodes_keys = list(cache_handler.cache[flow_id].keys())
        msg = f"{len(cache_nodes_keys)} Nodos en caché"
        bug_handler.default_on_error(
            flow_id, None, msg, console_level="trace", bug_level="info", success=True
        )

        # Inicializa una copia local de los nodos y su metadata
        self.set_nodes(flow_id, data)

        num_nodes_ok: int = 0  # conteo del número de nodos procesados
        attemps: int = 0  # contador de intentos del while para procesar el flujo completo
        t1 = time.time()  # inicializa el tiempo total de procesamiento de los nodos
        completed_nodes: list = []

        # mientras no estén todos los nodos procesados
        while num_nodes_ok < len(self.nodes):
            # print(num_nodes_ok, "<", len(self.nodes))
            attemps += 1
            for node_key, node_data in self.nodes.items():
                # Salto los nodos que están cargado
                if self.nodes[node_key]["loaded"]:
                    continue

                # * Salto los nodos output data cuando el check de deshabilitar está activado
                if disable_all_write_nodes and (node_data["type"] in [NodeType.OUTPUTDATA.value, NodeType.EXCEL.value]):
                    msg = "Se omite escritura de archivo para nodo {}".format(node_data["key"])
                    bug_handler.default_on_error(
                        flow_id, None, msg, console_level="trace", bug_level="info", success=True
                    )

                    # para que no entre dos veces en caso que el while haga mas de un intento
                    self.nodes[node_key]["loaded"] = True
                    num_nodes_ok += 1
                    completed_nodes.append(node_data["key"])
                    continue

                # Omito procesar los nodos hijos de un nodo que tuvo un error
                if self.nodes[node_key]["skip"]:
                    # self.node_data[n_key]['loaded'] = True # para que no entre dos veces en caso que el while haga mas de un intento
                    bug_handler.console(
                        "nodo {} saltado".format(node_data["key"]), "trace", flow_id
                    )
                    num_nodes_ok += 1
                    completed_nodes.append(node_data["key"])
                    continue

                # --------------------------------------------------
                # Dertermina si el/los nodos padres están cargados
                # --------------------------------------------------
                is_loaded: bool = False
                input_port: dict = {}  # almancena los df del mapeo de los puertos de entrada
                # parent_ports = []
                # Si es una entrada de datos que no tiene padre, se puede procesar
                if not node_data["parents"]:
                    # Omite los nodos de entrada de datos (sin puertos de entrada), ya que por consecuencia no tiene registro de nodos padres
                    if node_data["type"] in [
                        NodeType.INPUTDATA.value,
                        NodeType.DFMAKER.value,
                        NodeType.DATABASE.value,
                        NodeType.SOURCE.value,
                    ]:
                        is_loaded = True
                    else:
                        msg = "Se omite nodo {} sin entrada padre".format(node_data["key"])
                        bug_handler.default_on_error(
                            flow_id,
                            None,
                            msg,
                            console_level="trace",
                            bug_level="info",
                            success=True,
                        )

                        # para que no entre dos veces en caso que el while haga mas de un intento
                        self.nodes[node_key]["loaded"] = True
                        num_nodes_ok += 1
                        completed_nodes.append(node_data["key"])
                        self.set_skip_childs_recursive(flow_id, node_key, data)
                        continue
                else:  # Si el nodo tiene padres
                    # Compruebo si todos los padres tienen sus salidas cargadas
                    for parent in node_data["parents"]:
                        is_loaded = True  # incializo la carga en verdadero
                        # print(parent['from'], parent['from'] in cache_handler.cache[flow_id], cache_handler.cache[flow_id].keys())
                        # Si está la salida en el nodo padre
                        if self.nodes[parent["from"]]["output"] != None:
                            # if parent['from'] in cache_handler.cache[flow_id]:

                            # input_port[parent["topid"]] = cache_handler.cache[flow_id][parent["from"]]["pout"][parent["frompid"]]
                            parent_key = parent["from"]
                            parent_port = parent["frompid"]
                            parent_cache = cache_handler.get_node(
                                flow_id, parent_key
                            )  # nodo desde caché
                            
                            if (
                                parent_cache
                                and "pout" in parent_cache
                                and parent_port in parent_cache["pout"]
                            ):
                                input_port[parent["topid"]] = parent_cache["pout"][parent_port]
                            # else:
                            #     # TODO: error

                            # Almaceno en el mapeo de entrada del nodo el df asociado a la salida del padre
                            # input_port[parent['topid']] = self.node_data[parent['from']]['output'][parent['frompid']]
                            # parent_ports.append((parent['frompid'], self.node_data[parent['from']]))
                        else:  # Si al menos un padre no está procesado, etonces termina la iteración
                            # print('\n\n\n\n', 'x'*100, n_data['key'], parent['topid'], '--', parent['from'] , parent['frompid'] , '\n\n\n\n')
                            is_loaded = False  # si al menos uno no está cargado
                            break
                    # if n_data['name'] == 'Code':
                    # 	is_loaded = True
                # --------------------------------------------------
                # Si el nodo se puede procesar inicia el procesamiento
                # --------------------------------------------------
                # print(f'is_loaded: {is_loaded} / nodo: ', n_key)
                if is_loaded:
                    node_idx: int = self.nodes[node_key]["idx"]
                    node_name: str = data["nodeDataArray"][node_idx]["name"]
                    node_key: str = data["nodeDataArray"][node_idx]["key"]
                    self.cur_node_key = node_key

                    # print(f'PROCESANDO NODO {node_key}')

                    # --------------------------------------------------
                    # Actualizo los dtypes de la entrada con el dataframe de la salida del nodo anterior
                    # --------------------------------------------------
                    # Omite nodos de entrada de datos (sin puertos de entrada)
                    if node_data["type"] not in [
                        NodeType.INPUTDATA.value,
                        NodeType.DFMAKER.value,
                        NodeType.DATABASE.value,
                        NodeType.SOURCE.value,
                    ]:
                        for _, pin_name in enumerate(
                            data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"]
                        ):
                            if (
                                "dtypes"
                                in data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"][
                                    pin_name
                                ]
                                and pin_name in input_port
                            ):
                                dtypes_list = data["nodeDataArray"][node_idx]["meta"]["ports_map"][
                                    "pin"
                                ][pin_name]["dtypes"]

                                u_dtypes = self.update_inputs_dtypes(
                                    node_name,
                                    node_key,
                                    dtypes_list,
                                    input_port[pin_name],
                                )
                                data["nodeDataArray"][node_idx]["meta"]["ports_map"]["pin"][
                                    pin_name
                                ]["dtypes"] = u_dtypes
                                # print(pin_index, 'fin')

                    # --------------------------------------------------
                    # Valida si el nodo actual está en caché y si su configuración sigue siendo la misma
                    # --------------------------------------------------
                    node_cache = cache_handler.get_node(flow_id, node_key)
                    if (
                        node_cache 
                        and 
                        ("config" in node_cache and node_cache["config"] == json.dumps(data["nodeDataArray"][node_idx]["meta"]["config"], sort_keys=True))
                        and
                        (
                            "ports_config" not in node_cache
                            or 
                            ("ports_config" in node_cache and node_cache["ports_config"] == json.dumps(data["nodeDataArray"][node_idx]["meta"]["ports_config"], sort_keys=True))
                        )
                    ):
                        # await socket_server.emit('dataprep.node_processing', {
                        #     'flow_id': flow_id,
                        #     'key': n_key,
                        # })
                        # bug_handler.console(f'Nodo "{node_key}" saltado, para flujo flow_id: "{flow_id}"', 'info', flow_id, False)
                        # reset_childs = False
                        data["nodeDataArray"][node_idx]["meta"]["readed_from_cache"] = True
                        script_handler.script += node_cache["script"]
                        data["nodeDataArray"][node_idx]["meta"]["processed"] = True
                        # await socket_server.emit('dataprep.node_processed', {
                        #     'flow_id': flow_id,
                        #     'key': node_key,
                        #     'node': json.dumps(data['nodeDataArray'][idx], default=str),
                        #     # 'log': log_handler.log, # TODO: Hacer el log del nodo correspondiente
                        # })
                    # --------------------------------------------------
                    # Procesa el nodo correspondiente y actualiza los valores de los df
                    # --------------------------------------------------
                    else:
                        bug_handler.console(f"PROCESANDO NODO {node_key}", "-", flow_id)
                        if (
                            node_cache
                            and 
                            (
                                ("config" in node_cache and node_cache["config"] != json.dumps(data["nodeDataArray"][node_idx]["meta"]["config"], sort_keys=True))
                                or
                                ("ports_config" in node_cache and node_cache["ports_config"] != json.dumps(data["nodeDataArray"][node_idx]["meta"]["ports_config"], sort_keys=True))
                            )
                        ):
                            reseted_nodes = self.reset_childs_recursive(
                                flow_id, node_key, [node_key]
                            )
                            event_handler.emit_queue.put(
                                {
                                    "name": "dataprep.reseted_nodes",
                                    "data": {
                                        "flow_id": flow_id,
                                        "reseted_nodes": reseted_nodes,
                                    },
                                }
                            )

                        # await socket_server.emit('dataprep.node_processing', {
                        #     'flow_id': flow_id,
                        #     'key': n_key,
                        # })
                        data["nodeDataArray"][node_idx] = self.pipeline.exec(
                            flow_id, data["nodeDataArray"][node_idx], input_port
                        )
                        data["nodeDataArray"][node_idx]["meta"]["processed"] = True
                        event_handler.emit_queue.put(
                            {
                                "name": "dataprep.node_processed",
                                "data": {
                                    "flow_id": flow_id,
                                    "key": node_key,
                                    "node": json.dumps(
                                        data["nodeDataArray"][node_idx], default=str
                                    ),
                                    # 'log': log_handler.log, # TODO: Hacer el log del nodo correspondiente
                                },
                            }
                        )

                    # self.node_data[n_key]['output'] = full_df # Almaceno los df del mapeo de salida
                    # Almaceno los df del mapeo de salida
                    self.nodes[node_key]["output"] = True
                    # Fijo la bandera mara para marcar que el nodo está procesado
                    self.nodes[node_key]["loaded"] = True
                    # Aumento el contador para saber que ese nodo fue analizado y salir del while
                    num_nodes_ok += 1
                    completed_nodes.append(node_data["key"])

                    # --------------------------------------------------
                    # Valida si el nodo actual se registró en el singleton de bug con level==error, de estarlo se saltan los hijos de esos nodos
                    # --------------------------------------------------
                    has_error = (
                        next(
                            (
                                x
                                for x in bug_handler.bug
                                if x["node_key"] == node_key and x["level"] == "error"
                            ),
                            None,
                        )
                        != None
                    )
                    data["nodeDataArray"][node_idx]["meta"]["skipped"] = False
                    data["nodeDataArray"][node_idx]["meta"]["has_error"] = False
                    if has_error:
                        print("\n\n\n----------- has_error", has_error)
                        cache_handler.delete_node(flow_id, node_key)
                        data["nodeDataArray"][node_idx]["meta"]["has_error"] = True
                        self.set_skip_childs_recursive(flow_id, node_key, data)

                    # # Si ese nodo fue ejecutado nuevamente por algun cambio en la config, reseteo todos los hijos dependientes del mismo
                    # if reset_childs:
                    # 	# print(self.node_data[n_key]['childs'])
                    # 	# print('key: ', node_key, n_key)
                    # 	self.reset_childs_recursive(flow_id, n_key)

        # --------------------------------------------------
        # Fin del while y for principal
        # --------------------------------------------------
        cache_nodes_keys = list(cache_handler.cache[flow_id].keys())
        msg = f"Se almacenaron {len(cache_nodes_keys)} nodos en caché"
        # bug_handler.console(msg, 'debug', flow_id)
        bug_handler.default_on_error(
            flow_id, None, msg, console_level="debug", bug_level="info", success=True
        )

        msg = "Flujo procesado en {} segundos ".format(round(time.time() - t1, 3))
        bug_handler.default_on_error(
            flow_id, None, msg, console_level="debug", bug_level="info", success=True
        )

        # bug_handler.console(f'**** BUG **** {bug_handler.bug}', 'debug', flow_id)

        # Una vez que acaba la ejecución del flujo se conforma el script
        self.script = "\n".join(script_handler.script)
        # print('\n\n script', len(script_handler.script))
        # print(self.script)
        # # FIXME: No se puede, es más lento que la escritura del pickle en disco
        # t = time.time()
        # self.ultra = UltraDict(
        #     cache_handler.cache[flow_id],
        #     name=flow_id,
        #     recurse=True,
        #     shared_lock=True,
        #     # auto_unlink=True,
        # )
        # print(f"dump {time.time()-t} segundos")
        del self.nodes
        gc.collect()

        return data

    # ---------------------------------------------------------------------------------------
    # Actualiza los dtypes utilizando el df que se está recibiendo de entrada
    # y compara con lo que se tenía en la configuración, manejando tanto la
    # creación de campos que antes no existían, como la eliminación de campos que fueron eliminados

    def update_inputs_dtypes(self, node_name, node_key, current_dtypes, input_df: pd.DataFrame):
        # if node_name == 'Merge':
        # print('\ncurrent_dtypes')
        # print(current_dtypes)
        # print('\ninput_df')
        # print(input_df)

        # print('\nIteration')
        res = input_df.dtypes.to_frame("dtypes")
        res = res["dtypes"].astype(str).reset_index()
        # print('res:', res)
        updated_dtypes = {}
        for i, x in res.iterrows():
            updated_dtypes[x["index"]] = {
                "dtype": x["dtypes"],
                "selected": True,
                "order": i,
            }

        return updated_dtypes
        """
        if not len(current_dtypes):
            return current_dtypes

        # Si hay que crear campos nuevos se agregarán al final
        try:
            max_order =  max(list(map(lambda x: x['order'], current_dtypes.values())))
        except Exception as e:
            print('Error (builder): ', e)
            bug_handler.append({'flow_id':flow_id, 'success': False, 'node_key': None, 'level': 'error',
                                        'msg': 'No fue obtener el max de la lista de dtypes', 'exception': str(e)})
            return current_dtypes

        for i,x in res.iterrows():
            if x['index'] in current_dtypes: # si el campo en la salida está en el pin de entrada, sólo actualizo el tipo de dato
                if node_name != 'Select': # los select, al permitir cambiar los datatypes no deben actualizarse
                    current_dtypes[x['index']]['dtype'] = x['dtypes']
            else: # si el campo no está, es porque se editó el flujo en algun punto intermedio y se debe crear el campo
                # del current_dtypes[x['index']]
                max_order += 1
                current_dtypes[x['index']] = {'dtype': x['dtypes'], 'selected': True, 'order': max_order}
                print('previamente no existía el campo "{}" en el nodo "{}", se agrega'.format(x['index'], node_name))
                bug_handler.append({'flow_id':flow_id, 'success': True, 'node_key': node_key, 'level': 'info',
                                        'msg': 'Campo "{}" no existía en el nodo "{}" previamente, se agrega'.format(x['index'], node_name), 'exception': ''})
                # print('Campo "{}" no existe en nodo "{}" será omitido'.format(x['index'], node_name))
        # print('\n\n\ncurrent_dtypes:\n')
        # print(current_dtypes)
        # Extraigo los campos que antes existían y ya no
        removed_fields = list(set(current_dtypes.keys()) - set(res['index'].tolist()))
        # Remuevo los campos que ya no existen
        # current_dtypes = dict(filter(lambda i: i[0] in res['index'].tolist(), current_dtypes.items()))
        for rf in removed_fields:
            to_remove = current_dtypes[rf]
            # print(rf, to_remove)
            bug_handler.append({'flow_id':flow_id, 'success': True, 'node_key': node_key, 'level': 'warning',
                                        'msg': 'Ya no existe el campo "{}" en el nodo "{}", se elimina de sus dtypes'.format(rf, node_name), 'exception': ''})
            del current_dtypes[rf]

        # print('\ncurrent_dtypes (modified):')
        # print(current_dtypes)
        return current_dtypes
        """

    def remove_flow_from_cache(self, key: str):
        if key in cache_handler.cache:
            del cache_handler.cache[key]

    def remove_nodes_from_cache(self, flow_id: str, node_keys: list[str]):
        removeds = []
        if flow_id in cache_handler.cache:
            for nodekey in node_keys:
                if nodekey in cache_handler.cache[flow_id]:
                    removeds.append(nodekey)
                    del cache_handler.cache[flow_id][nodekey]
        return removeds

    # Actualiza node['meta']['ports_map']['pout'][port_name]['summary']
    def load_detailed_view(self, flow_id: str, node_key: str, port_name: str):
        if flow_id in cache_handler.cache and node_key in cache_handler.cache[flow_id]:
            df = cache_handler.cache[flow_id][node_key]["pout"][port_name]
            return utilities.viz_summary(df)
        return {}

    # Actualiza node['meta']['ports_map']['pout'][port_name]['describe']
    def load_column_view(self, flow_id: str, node_key: str, port_name: str):
        if flow_id in cache_handler.cache and node_key in cache_handler.cache[flow_id]:
            df = cache_handler.cache[flow_id][node_key]["pout"][port_name]
            return utilities.get_central_tendency_measures(df)
        return {}

    def modify_node(self, flow_id: str, node_key: str, node: dict, port_name: str):            
        cached_node = cache_handler.get_node(flow_id, node_key)
        if cached_node and "pout" in cached_node and port_name in cached_node["pout"]:
            port_df: pd.DataFrame = cached_node["pout"][port_name]
            port_config: dict = utilities.get_table_config(node["meta"], port_name, flow_id, node_key)
            # for port_name in node["meta"]["ports_map"]["pout"].keys():
            node["meta"]["ports_map"]["pout"][port_name]["head"] = utilities.get_head_of_df_as_list(port_df, port_config, flow_id, node_key, port_name)
        return {"flow_id": flow_id, "node_key": node_key, "node": node}

if __name__ == "__main__":
    b = Builder()
    m = b.load_model()
    print(m)
