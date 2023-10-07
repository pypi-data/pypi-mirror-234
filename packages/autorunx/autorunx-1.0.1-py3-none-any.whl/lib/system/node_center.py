
import sys,os
import globals


user_node_set=set()

"""
key: node id
value: node
"""
node_dict={}


def init(**kwargs):
    # init user_node_set
    global user_node_set
    import os
    lib_root=os.path.join(os.path.dirname(__file__),"../")
    node_class_paths=[os.path.join(lib_root,type) for type in ['dataio','dataprocess','flowcontrol','flowfunction']]
    for node_root in node_class_paths:
        for node_name in os.listdir(node_root):
            if os.path.isfile(os.path.join(node_root,node_name)) and node_name!='__init__.py':
                user_node_set.add(node_name.replace('.py',''))
    return None


def put(key,value,**kwargs):
    node_dict[key]=value


def get(key,**kwargs):
    return node_dict[key]


def has(key,**kwargs):
    return key in node_dict


def generate(key,**kwargs):
    """
    key: node_name, node's filename but bot include extension, module name
    """
    if key in user_node_set:
        return globals.import_module(key)
    else:
        raise Exception('No "{}" module or node'.format(key))


def get_or_generate(id,node_name,**kwargs):
    """
    id: node_id or node_name, typically this is the node_id
    node_name: node_name, node's filename but bot include extension, also called the module name
    """
    if id in node_dict:
        return node_dict[id]
    else:
        return generate(node_name)










































