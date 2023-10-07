
import sys,os
import globals

import copy


nodes_config={}  # key: config's id. value: config
edges_config={}

flow_nodes_config={}
data_nodes_config={}

start_node_config=None  # only one
end_node_config=None  # only one

dtio_nodes_config={}
dtpc_nodes_config={}
ctrl_nodes_config={}
func_nodes_config={}

nodes_link_input={}  # node 输入参数(input)中被链接的参数名。 key:node_id-->value:param_list
nodes_link_input_sourcemapping={}  # node 输入参数(input)中被链接的参数值数据来源。key:node_id1.input.param_name-->value:node_id2.output.param_name


is_active=False
running_node_id=""
runnint_node_config=None



def init(**kwargs):
    # ini config
    global nodes_config,edges_config

    # input config
    if "node_list" in kwargs:
        node_list=kwargs["node_list"]
        for node in node_list:
            nodes_config[node['id']]=node
    if "edge_list" in kwargs:
        edge_list=kwargs["edge_list"]
        for edge in edge_list:
            edges_config[edge['id']]=edge
    
    if "node_config" in kwargs:
        nodes_config=kwargs["node_config"]
    if "edge_config" in kwargs:
        edges_config=kwargs["edge_config"]
    
    global start_node_config,end_node_config,flow_nodes_config,data_nodes_config
    global dtio_nodes_config,dtpc_nodes_config,ctrl_nodes_config,func_nodes_config

    for key in nodes_config:
        if nodes_config[key]["node_type"]=="start":
            flow_nodes_config[key]=nodes_config[key]
            start_node_config=nodes_config[key]
        elif nodes_config[key]["node_type"]=="end":
            flow_nodes_config[key]=nodes_config[key]
            end_node_config=nodes_config[key]
        elif nodes_config[key]["node_type"]=="dtio":
            data_nodes_config[key]=nodes_config[key]
            dtio_nodes_config[key]=nodes_config[key]
        elif nodes_config[key]["node_type"]=="dtpc":
            data_nodes_config[key]=nodes_config[key]
            dtpc_nodes_config[key]=nodes_config[key]
        elif nodes_config[key]["node_type"]=="ctrl":
            flow_nodes_config[key]=nodes_config[key]
            ctrl_nodes_config[key]=nodes_config[key]
        else:
        # elif nodes_config[key]["node_type"]=="func":
            flow_nodes_config[key]=nodes_config[key]
            func_nodes_config[key]=nodes_config[key]
    
    global nodes_link_input,nodes_link_input_sourcemapping
    
    for key in edges_config:
        pre_id=str(edges_config[key]["pre_id"])
        nxt_id=str(edges_config[key]["nxt_id"])
        output_index=pre_id.find(".output.")
        input_index=nxt_id.find(".input.")
        if input_index>-1 and output_index>-1:
            nodes_link_input_sourcemapping[nxt_id]=pre_id
            node_id=nxt_id[0:input_index]
            if node_id in nodes_link_input:
                nodes_link_input[node_id].append(nxt_id[input_index+7:])
            else:
                nodes_link_input[node_id]=[nxt_id[input_index+7:]]


def start(**kwargs):
    data_start()
    flow_start()


def data_start(**kwargs):
    node_to_be_run=[_ for _ in data_nodes_config]
    while len(node_to_be_run)>0:
        length=len(node_to_be_run)
        for id in copy.deepcopy(node_to_be_run):
            if not is_node_linkin_data_ready(id):
                continue
            data(id)
            node_to_be_run.remove(id)
        if length==len(node_to_be_run):
            break    


def flow_start(**kwargs):
    global is_active
    is_active=True
    flow(start_node_config["id"])


def flow_end(**kwargs):
    global is_active
    is_active=False
    # exit()


def flow(id,**kwargs):
    if id not in flow_nodes_config or not is_active:
        # is not flow about
        return
    # load input params
    node_config=copy.deepcopy(nodes_config[id])
    if not is_node_linkin_data_ready(id):
        print("{}.{}: Error!!! Node input data missing!!!".format(id,node_config["node_name"]))
        return
    input_data=get_node_linkin_data(id)
    node_config["input"]={**node_config["input"],**input_data}  # Notice the order, input_data must be at the end
    # print("node_input_data",node_config["input"],input_data)
    # node start
    node=globals.node_center.get_or_generate(id,node_config["node_name"])
    @globals.aop(id=id,name=node_config["node_name"])
    def node_run(*args,**kwargs):
        global running_node_id,runnint_node_config
        tmp_running_node_id=running_node_id
        tmp_runnint_node_config=runnint_node_config
        running_node_id=id
        runnint_node_config=copy.deepcopy(nodes_config[id])
        results = node.run(*args,**kwargs)
        running_node_id=tmp_running_node_id
        runnint_node_config=tmp_runnint_node_config
        return results
    results=node_run(**node_config["input"])
    # store node and keep alive
    if results is None or not isinstance(results,dict):
        results={}
    if "keep_alive" in results and results["keep_alive"]==True:
        globals.node_center.put(id,node)
    # store output params
    put_node_linkout_data(id,results)
    # start next node
    if  id in ctrl_nodes_config or id == start_node_config["id"] or (end_node_config is not None and id == end_node_config["id"]):
        return
    if "nxt_edge_id" not in node_config or len(node_config["nxt_edge_id"])<=0:
        return
    edge_id=node_config["nxt_edge_id"][0]
    if edge_id in edges_config:
        flow(edges_config[edge_id]["nxt_id"])


def data(id,**kwargs):
    if id not in dtpc_nodes_config and id not in dtio_nodes_config:
        # is not data about
        return
    node_config=copy.deepcopy(nodes_config[id])
    if not is_node_linkin_data_ready(id):
        return
    input_data=get_node_linkin_data(id)
    node_config["input"]={**node_config["input"],**input_data}  # Notice the order, input_data must be at the end
    # print("node_input_data",node_config["input"],input_data)
    # node start
    node=globals.node_center.get_or_generate(id,node_config["node_name"])
    @globals.aop(id=id,name=node_config["node_name"])
    def node_run(*args,**kwargs):
        global running_node_id,runnint_node_config
        running_node_id=id
        runnint_node_config=copy.deepcopy(nodes_config[id])
        results = node.run(*args,**kwargs)
        running_node_id=""
        runnint_node_config=None
        return results
    results=node_run(**node_config["input"])
    # store node and keep alive
    if results is None or not isinstance(results,dict):
        results={}
    if "keep_alive" in results and results["keep_alive"]==True:
        globals.node_center.put(id,node)
    # store output params
    put_node_linkout_data(id,results)


def is_node_linkin_data_ready(id,**kwargs):
    if id not in nodes_link_input:
        return True
    for param_name in nodes_link_input[id]:
        data_key=nodes_link_input_sourcemapping["{}.input.{}".format(id,param_name)]
        if not globals.data_center.has(data_key):
            # Error! 缺少数据
            return False
    return True


def get_node_linkin_data(id,**kwargs):
    if id not in nodes_link_input:
        return {}
    result={}
    for param_name in nodes_link_input[id]:
        data_key=nodes_link_input_sourcemapping["{}.input.{}".format(id,param_name)]
        # print(id,param_name,data_key)
        if not globals.data_center.has(data_key):
            # Error! 缺少数据
            print("Error! 缺少数据")
            # return {}
            pass
        else:
            result[param_name]=globals.data_center.get(data_key)
    return result


def put_node_linkout_data(id,output_data,**kwargs):
    dtpc_to_be_run=[]
    if output_data is None or not isinstance(output_data,dict):
        return
    for key in output_data:
        data_id="{}.output.{}".format(id,key)
        globals.data_center.put(data_id,output_data[key])
        for edge_id in edges_config:
            edge=edges_config[edge_id]
            nxt_node_id=edge["nxt_id"][0:edge["nxt_id"].find(".input.")]
            if data_id==edge["pre_id"] and nxt_node_id in dtpc_nodes_config:
                dtpc_to_be_run.append(nxt_node_id)
    while len(dtpc_to_be_run)>0:
        length=len(dtpc_to_be_run)
        for dtpc_id in copy.deepcopy(dtpc_to_be_run):
            if not is_node_linkin_data_ready(dtpc_id):
                continue
            data(dtpc_id)
            dtpc_to_be_run.remove(dtpc_id)
        if length==len(dtpc_to_be_run):
            break








































