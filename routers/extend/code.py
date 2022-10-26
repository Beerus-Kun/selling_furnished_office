import string
import random
import re
import os
def getCode():
    try:
        fin = open('routers/extend/code.txt', 'r')
        data = fin.read().splitlines(True)

        fout = open('routers/extend/code.txt', 'w')
        fout.writelines(data[1:])
        return data[0]
    except Exception as e:
        print(e)

def saveCode():
    try:
        char = string.ascii_uppercase + string.digits
        char = char[:10]
        a = []

        f = open("code.txt", "w")

        def genCode(code, limit):
            if len(code) == limit:
                # f.write(code,"\n")
                a.append(code)
            else:
                for i in char:
                    if i not in code:
                        genCode(code + i, limit)
        genCode("", 6)
        random.shuffle(a)
        for i in a:
            f.write(i+ "\n")
        f.close()
    except Exception as e:
        print(e)

def str2list(txt:str):
    return txt[1:-1].replace('"','').split(',')

def standardized(a:str):
    whitespace = r"\s+"
    # Replace all mathces with an empty string
    nospaces = re.sub(whitespace, " ", a).strip()
    return nospaces