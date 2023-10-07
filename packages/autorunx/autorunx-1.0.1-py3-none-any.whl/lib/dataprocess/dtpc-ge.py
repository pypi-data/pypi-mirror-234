







def run(**kwargs):
    number_1=0
    number_2=0
    if "number_1" in kwargs:
        number_1=kwargs["number_1"]
    if "number_2" in kwargs:
        number_2=kwargs["number_2"]
    return {"result":number_1>=number_2}


































