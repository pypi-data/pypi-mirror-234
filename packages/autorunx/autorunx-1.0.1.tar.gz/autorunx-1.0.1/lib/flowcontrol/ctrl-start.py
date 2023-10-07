
import sys,os
import globals
import copy



def run(**kwargs):
    # print("control start...")
    node_config=copy.deepcopy(globals.engine.runnint_node_config)
    if "nxt_edge_id" not in node_config or len(node_config["nxt_edge_id"])<=0:
        return
    edge_id=node_config["nxt_edge_id"][0]
    if edge_id in globals.engine.edges_config:
        globals.engine.flow(globals.engine.edges_config[edge_id]["nxt_id"])
    return {}





















