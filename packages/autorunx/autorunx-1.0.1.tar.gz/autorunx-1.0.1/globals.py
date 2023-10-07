# global 

import sys,os
# or all platform. On window platform, sys.path[0] is same with basedir below:
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,basedir)
sys.path.append(os.path.join(sys.path[0],'lib/dataio'))
sys.path.append(os.path.join(sys.path[0],'lib/dataprocess'))
sys.path.append(os.path.join(sys.path[0],'lib/flowcontrol'))
sys.path.append(os.path.join(sys.path[0],'lib/flowfunction'))
sys.path.append(os.path.join(sys.path[0],'lib/system'))

from importlib import import_module


# ====================================== data_center module ======================================


# data center
data_center=None


def init_data_center(**kwargs):
    global data_center
    DATA_CENTER_MODULE_NAME="lib.system.data_center"
    data_center=import_module(DATA_CENTER_MODULE_NAME)
    data_center.init()
    



# ====================================== node_center module ======================================


# node center
node_center=None


def init_node_center(**kwargs):
    global node_center
    NODE_CENTER_MODULE_NAME="lib.system.node_center"
    node_center=import_module(NODE_CENTER_MODULE_NAME)
    node_center.init()



# ====================================== log module ======================================


# log module
log_module=None
common_log=None
func_log=None

def init_log(**kwargs):
    """log module"""
    # get config and ini constant
    # global COMMON_LOG_FILE,FUNC_LOG_FILE,LOG_MODULE_NAME
    LOG_MODULE_NAME="lib.system.log"
    COMMON_LOG_FILE="log/common.log"      # common log, all(log) in one.
    FUNC_LOG_FILE="log/log.log"        # pure log, node log output
    if "LOG_MODULE_NAME" in kwargs:
        LOG_MODULE_NAME=kwargs['LOG_MODULE_NAME']
    if "COMMON_LOG_FILE" in kwargs:
        COMMON_LOG_FILE=kwargs['COMMON_LOG_FILE']
    if "FUNC_LOG_FILE" in kwargs:
        FUNC_LOG_FILE=kwargs['FUNC_LOG_FILE']
    # import module
    global log_module
    log_module=import_module(LOG_MODULE_NAME)
    # ini module
    log_module.init(COMMON_LOG_FILE=COMMON_LOG_FILE,FUNC_LOG_FILE=FUNC_LOG_FILE)
    # ini module function
    global common_log,func_log
    common_log=log_module.common_log
    func_log=log_module.func_log



# ====================================== aop module ======================================


# aop module
aop_module=None
aop=None

def init_aop(**kwargs):
    """aop module"""
    # get config and ini constant
    # global AOP_LOG_FILE,AOP_MODULE_NAME
    AOP_MODULE_NAME="lib.system.aop"
    AOP_LOG_FILE="log/aop.log"         # aop log, use to debug or record program flow
    if "AOP_MODULE_NAME" in kwargs:
        AOP_MODULE_NAME=kwargs['AOP_MODULE_NAME']
    if "AOP_LOG_FILE" in kwargs:
        AOP_LOG_FILE=kwargs['AOP_LOG_FILE']
    # import module
    global aop_module
    aop_module=import_module(AOP_MODULE_NAME)
    # ini module
    aop_module.init(AOP_LOG_FILE=AOP_LOG_FILE)
    # ini module function
    global aop
    aop=aop_module.aop



# ====================================== engine module ======================================


# engine
engine=None
def init_engine(**kwargs):
    global engine
    ENGINE_MODULE_NAME="lib.system.engine"
    engine=import_module(ENGINE_MODULE_NAME)
    # params: graph:{node_list:[],edge_list:[]}
    engine.init(**kwargs)



# ====================================== init & start ======================================


def init(**kwargs):
    init_data_center()
    init_node_center()
    if "common" in kwargs and "aop" in kwargs["common"]:
        init_aop(**kwargs["common"]["aop"])
    else:
        init_aop()
    if "common" in kwargs and "log" in kwargs["common"]:
        init_log(**kwargs["common"]["log"])
    else:
        init_log()
    if "graph" in kwargs:
        init_engine(**kwargs["graph"])
    else:
        print("Error: Invalid profile!")
    

def start():
    engine.start()























