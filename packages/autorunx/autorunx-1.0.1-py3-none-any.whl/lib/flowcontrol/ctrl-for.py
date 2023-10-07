
import sys,os
import globals
import copy


def run(**kwargs):
    # print("control for...")
    node_config=copy.deepcopy(globals.engine.runnint_node_config)
    start_index=0
    end_index=5
    step=1
    loop_edge_id=""
    if "start_index" in kwargs:
        start_index=int(kwargs["start_index"])
    if "end_index" in kwargs:
        end_index=int(kwargs["end_index"])
    if "step" in kwargs:
        step=int(kwargs["step"])
    if "loop_edge_id" in node_config["output"]:
        loop_edge_id=node_config["output"]["loop_edge_id"]
    # find edge and cover config
    for key in globals.engine.edges_config:
        edge=globals.engine.edges_config[key]
        if edge["pre_id"]=="{}.output.loop_edge_id".format(globals.engine.running_node_id):
            loop_edge_id=key
            break
    # loop 
    loop_node_id=None
    if loop_edge_id in globals.engine.edges_config:
        loop_node_id=globals.engine.edges_config[loop_edge_id]["nxt_id"]
    for index in range(start_index,end_index,step):
        cur_node_result={"index":index}
        globals.engine.put_node_linkout_data(node_config["id"],cur_node_result)
        if loop_node_id is not None:
            globals.engine.flow(loop_node_id)
    # loop end. flow next node
    if "nxt_edge_id" not in node_config or len(node_config["nxt_edge_id"])<=0:
        return
    edge_id=node_config["nxt_edge_id"][0]
    if edge_id in globals.engine.edges_config:
        globals.engine.flow(globals.engine.edges_config[edge_id]["nxt_id"])
    return {}





















