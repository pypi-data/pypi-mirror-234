







def run(**kwargs):
    bool_1=False
    bool_2=False
    if "bool_1" in kwargs:
        bool_1=kwargs["bool_1"]
    if "bool_2" in kwargs:
        bool_2=kwargs["bool_2"]
    return {"result":bool_1 or bool_2}


































