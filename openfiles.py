# file for opening certain files - has different variations

def open_a_file(path : str) :


    with open(path,"r", encoding="utf-8") as json_file:
        contents = json_file.read()





    return contents