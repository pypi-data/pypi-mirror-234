"""
evaluator.py

This file is used to evaluate task 2A of AstroTinker Bot theme.
It generates the dump_txt.txt file which is used in the simulation.

"""

def toBinary(a):
    l,m=[],[]
    for i in a:
        l.append(ord(i))
    for i in l:
        m.append(bin(i)[2:].zfill(8))
    return m


def evaluate():
    result = {}
    text = input("Enter the text: ")

    if len(text) <= 10:
        data = toBinary(text)
        with open('simulation/modelsim/dump_txt.txt', 'w') as f:
            for i in data:
                f.write(str(0))
                f.write('\n')
                for j in i:
                    f.write(j)
                    f.write('\n')
                f.write(str(1))
                f.write('\n')

    else:
        print("Entered text size is greater than 10!")

    result["generate"] = False
    return result
