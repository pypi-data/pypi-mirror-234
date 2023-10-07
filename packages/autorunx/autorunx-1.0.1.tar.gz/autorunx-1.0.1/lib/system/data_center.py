
import sys,os
import globals

import copy

"""
key: data id
value: data value
"""
data_dict={}


def init(**kwargs):
    pass


def put(key,value,**kwargs):
    data_dict[key]=copy.deepcopy(value)
    # print("put",key,data_dict[key])


def get(key,**kwargs):
    # print("get",key,data_dict[key])
    return copy.deepcopy(data_dict[key])


def get_dict_by_prefix(key,**kwargs):
    tmp_dict={}
    for k in data_dict:
        if str(k).startswith(key):
            tmp_dict[k]=copy.deepcopy(data_dict[k])
    return tmp_dict


def has(key,**kwargs):
    return key in data_dict



































