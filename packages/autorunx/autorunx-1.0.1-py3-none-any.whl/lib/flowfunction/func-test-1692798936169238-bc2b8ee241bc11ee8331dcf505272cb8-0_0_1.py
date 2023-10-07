
import globals



def run(**kwargs):
    globals.func_log(msg="func test start...")
    params=""
    for k in kwargs:
        params="{}{}: {}".format("" if params=="" else params+", ",k,kwargs[k])
    globals.func_log(msg="params: { "+params+" }")
    globals.func_log(msg="func test end...")
    return {**kwargs}

























