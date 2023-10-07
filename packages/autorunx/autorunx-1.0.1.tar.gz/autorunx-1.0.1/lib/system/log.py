
import sys,os
import globals

import datetime


COMMON_LOG_FILE="log/common.log"      # common log, all(log) in one.
FUNC_LOG_FILE="log/log.log"        # pure log, func log output


def init(**kwargs):
    global FUNC_LOG_FILE,COMMON_LOG_FILE
    if "COMMON_LOG_FILE" in kwargs:
        COMMON_LOG_FILE=kwargs['COMMON_LOG_FILE']
    if "FUNC_LOG_FILE" in kwargs:
        FUNC_LOG_FILE=kwargs['FUNC_LOG_FILE']
    for filefullpath in [COMMON_LOG_FILE,FUNC_LOG_FILE]:
        if len(filefullpath.split('/'))>1:
            [path,filename] = os.path.split(filefullpath)
            # print(path,filename)
            if not os.path.exists(path):
                os.makedirs(path)


def common_log(**kwargs):
    msg=kwargs['msg']
    # common log
    with open(COMMON_LOG_FILE,"+a",encoding="utf-8") as f:
        f.write(msg)
        # print(msg,end="")


def func_log(**kwargs):
    """
    kw:
    - msg: must, log message
    - second_log_file: optional
    """
    msg=kwargs['msg']
    msg="[{}]: {}\n".format(datetime.datetime.now(),msg)
    print(msg,end="")
    # func log
    with open(FUNC_LOG_FILE,"+a",encoding="utf-8") as f:
        f.write(msg)
    # common log
    common_log(msg=msg)
    # second log file
    if "second_log_file" in kwargs:
        if len(kwargs['second_log_file'].split('/'))>1:
            [path,filename] = os.path.split(kwargs['second_log_file'])
            if not os.path.exists(path):
                os.makedirs(path)
        with open(kwargs['second_log_file'],"+a",encoding="utf-8") as f:
            f.write(msg)


# init(COMMON_LOG_FILE="log/common-log.log")
# func_log(msg="hello func!")





