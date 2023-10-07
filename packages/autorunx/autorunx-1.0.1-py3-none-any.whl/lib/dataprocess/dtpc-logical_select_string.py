







def run(**kwargs):
    bool=False
    string_1=""
    string_2=""
    if "bool" in kwargs:
        bool=kwargs["bool"]
    if "string_1" in kwargs:
        string_1=kwargs["string_1"]
    if "string_2" in kwargs:
        string_2=kwargs["string_2"]
    return {"result":string_1 if bool else string_2}


































