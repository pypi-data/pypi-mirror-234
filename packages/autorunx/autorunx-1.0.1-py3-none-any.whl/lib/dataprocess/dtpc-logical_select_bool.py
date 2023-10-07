







def run(**kwargs):
    bool=False
    bool_1=True
    bool_2=False
    if "bool" in kwargs:
        bool=kwargs["bool"]
    if "bool_1" in kwargs:
        bool_1=kwargs["bool_1"]
    if "bool_2" in kwargs:
        bool_2=kwargs["bool_2"]
    return {"result":bool_1 if bool else bool_2}


































