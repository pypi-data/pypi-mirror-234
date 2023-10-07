







def run(**kwargs):
    string_1=""
    string_2=""
    if "string_1" in kwargs:
        string_1=kwargs["string_1"]
    if "string_2" in kwargs:
        string_2=kwargs["string_2"]
    return {"result":string_1==string_2}


































