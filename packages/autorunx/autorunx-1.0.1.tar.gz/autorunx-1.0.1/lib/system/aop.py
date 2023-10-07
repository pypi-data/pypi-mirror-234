
import sys,os
import globals

from functools import wraps
import os
import datetime


# config
AOP_LOG_FILE="log/aop.log"
LOG_OPEN=True  # disable



def init(**kwargs):
    global AOP_LOG_FILE,LOG_OPEN
    if "AOP_LOG_FILE" in kwargs:
        AOP_LOG_FILE=kwargs['AOP_LOG_FILE']
    if "LOG_OPEN" in kwargs:
        LOG_OPEN=kwargs['LOG_OPEN']
    if len(AOP_LOG_FILE.split('/'))>1:
        [path,filename] = os.path.split(AOP_LOG_FILE)
        # print(path,filename)
        if not os.path.exists(path):
            os.makedirs(path)


def log(msg):
    msg="[{}][aop]: {}\n".format(datetime.datetime.now(),msg)
    if not LOG_OPEN:
        # print(msg,end="")
        return
    # aop log
    with open(AOP_LOG_FILE,"+a",encoding="utf-8") as f:
        f.write(msg)
        # print(msg,end="")
    # common log
    if globals.common_log:
        globals.common_log(msg=msg)


def aop(id,name):
    def c(func):
        @wraps(func)
        def b(*args, **kwargs):
            log('{}.{}  node id:     {}'.format(id,name,id))
            log('{}.{}  node name:   {}'.format(id,name,name))
            log('{}.{}  node params: args={}, kwargs={}'.format(id,name,args, kwargs))
            log('{}.{}  node start...'.format(id,name))
            results = func(*args, **kwargs)
            log('{}.{}  node end...'.format(id,name))
            log('{}.{}  node return  results: {}'.format(id,name,results))
            return results
        return b
    return c


# Usage:
# @aop(name=os.path.basename(__file__))
# def a(name, age, lang):
#     print('函数执行中。。。')
#     return "函数结束返回值：我是 {}, 今年{}岁, 讲{}.".format(name, age,lang), "end"

# print(a('A', 24, lang="en"))
# print(a('B', 24, lang="ch"))














