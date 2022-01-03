import re
import numpy as np

def get_color(path):
    color = []
    rgb = lambda x: round(float(x) * 255.)
    with open(path) as f:
        for line in f.readlines():
            if re.match('Kd ', line):
                color.append( list(map(rgb, line.strip().split(' ')[1:])) )
    return color

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def get_verts(path):
    colors = get_color(re.sub('.obj', '.mtl', path))
    verts, faces, facesNbr = [], [], []
    i = 0
    toInt = lambda i: int(i) - 1
    with open(path) as f:
        for line in f.readlines():
            if re.match('v ', line):
                verts.append( [i * -1 for i in list(map(float, line.strip().split(' ')[1:]))] )
            elif re.match('f ', line):
                i += 1
                faces.append( list(map(toInt, line.strip().split(' ')[1:])) )
            elif re.match('usemtl', line):
                facesNbr.append(i)
        facesNbr.append(i)
    return np.array(verts), np.array(faces), colors, facesNbr
