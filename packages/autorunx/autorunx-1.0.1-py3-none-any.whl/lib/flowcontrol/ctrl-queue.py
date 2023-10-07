
import sys,os
import globals
import copy


def run(**kwargs):
    # print("control queue...")
    node_config=copy.deepcopy(globals.engine.runnint_node_config)
    if "nxt_edge_id" not in node_config:
        return
    for edge_id in node_config["nxt_edge_id"]:
        if edge_id in globals.engine.edges_config:
            globals.engine.flow(globals.engine.edges_config[edge_id]["nxt_id"])
    return {}





















