# # Open a file with access mode 'a'
# file_object = open('code.txt', 'a')
# # Append 'hello' at the end of file
# file_object.write('hello\n')
# file_object.write('hello1\n')
# file_object.write('hello2\n')
# file_object.write('hello3\n')
# # Close the file
# file_object.close()

# #open and read the file after the appending:
# f = open("code.txt", "r")
# print(f.readline())
# f.close()

import string
import random

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


# with open('code.txt', 'r') as fin:
#     data = fin.read().splitlines(True)
# with open('code.txt', 'w') as fout:
#     fout.writelines(data[1:])