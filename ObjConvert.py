import pyperclip
import random
import math

def get_obj(path,scale,offset):
    file = open(path)
    vertex_table = []
    edge_table = []
    face_table = []
    faces_color = []
    
    with file as f:
        for l in f:
            if l[0] == "v" and l[1] == " ":
                v3 = l.partition(" ")[2]
                v3 = v3.split(" ",3)
                v3[2] = v3[2].removesuffix("\n")
                for s in range(3):
                    v3[s] = float(v3[s])
                    v3[s] *= scale
                v3[1] *= -1
                v3[2] *= -1
                vertex_table.append(v3)
            if l[0] == "l":
                e3 = l.partition(" ")[2]
                e3 = e3.split(" ",2)
                e3[1] = e3[1].removesuffix("\n")
                for s in range(2):
                    e3[s] = int(e3[s])+offset-1
                edge_table.append(e3)
            if l[0] == "f":
                f3 = l.partition(" ")[2]
                if f3.count(" ") == 2:
                    f3 = f3.split(" ",3)
                    f3[2] = f3[2].removesuffix("\n")
                    for s in range(3):
                        f3[s] = int(f3[s])+offset-1
                elif f3.count(" ") == 3:
                    f3 = f3.split(" ",4)
                    f3[3] = f3[3].removesuffix("\n")
                    for s in range(4):
                        f3[s] = int(f3[s])+offset-1
                face_table.append(f3)

    for v in range(len(vertex_table)):
        value = vertex_table[v][1]
        c = str(hex(abs(int(value))))[2:]
        while len(c) != 6:
            c = c+"0"
        #faces_color.append("#"+c)
        faces_color.append((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        #faces_color.append((0,0,0))
    return(vertex_table,edge_table,face_table,faces_color)