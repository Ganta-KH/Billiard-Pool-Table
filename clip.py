import numpy as np
from tools import rot_mat

def clipping(projectedT, table_3D, clip, facesT, r, W, H):
    newFaces = []
    for count, face in enumerate(facesT[clip]):
        for f in face:
            if any([ (0.1 < projectedT[f, 0] < W) and (0.1 < projectedT[f, 1] < H) and table_3D[f, 2] >= r]):
                newFaces.append(count)
                break     
    return np.array(newFaces)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def CrossProduct(point_3D, facesT):
    # Cross Production
    A = point_3D[facesT[..., 1]] - point_3D[facesT[..., 0]]
    B = point_3D[facesT[..., 2]] - point_3D[facesT[..., 0]]
    N = np.zeros_like(A)

    # Calculate Normals
    N[..., 0] = A[..., 1] * B[..., 2] - A[..., 2] * B[..., 1]
    N[..., 1] = A[..., 2] * B[..., 0] - A[..., 0] * B[..., 2]
    N[..., 2] = A[..., 0] * B[..., 1] - A[..., 1] * B[..., 0]

    L = np.sqrt(N[..., 0] ** 2 + N[..., 1] ** 2 + N[..., 2] ** 2)
    L[L == 0] = .005

    N[..., 0] = np.divide(N[..., 0], L)
    N[..., 1] = np.divide(N[..., 1], L)
    N[..., 2] = np.divide(N[..., 2], L)

    return N

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def DotProduct(point_3D, facesT, camera, N):
    pos = np.array(camera.pos)
    pos = np.dot(rot_mat(*camera.rot), pos)

    N = np.multiply(N, (point_3D[facesT[..., 0]] - pos))
    N = N.sum(axis=1)
    
    return np.where(N < 0.)[0]

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def Zfar(points_3D, facesT):
    depth = np.array(list(map(lambda i: (points_3D[i[0], 2] + points_3D[i[1], 2] + points_3D[i[2], 2]) / 3., facesT)))
    return np.argsort(depth)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def Zfarr(points_3D, facesT, pos):
    L = lambda f: min(np.sqrt((points_3D[f[0], 0] - pos[0]) ** 2 + (points_3D[f[0], 1] - pos[1]) ** 2 + (points_3D[f[0], 2] - pos[2]) ** 2),
                      np.sqrt((points_3D[f[1], 0] - pos[0]) ** 2 + (points_3D[f[1], 1] - pos[1]) ** 2 + (points_3D[f[1], 2] - pos[2]) ** 2),
                      np.sqrt((points_3D[f[2], 0] - pos[0]) ** 2 + (points_3D[f[2], 1] - pos[1]) ** 2 + (points_3D[f[2], 2] - pos[2]) ** 2))
    Mdist = np.array(list(map(L, facesT)))
    return np.argsort(Mdist)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def Zfarrr(Balls, pos):
    pos = np.array(pos)
    clip = [np.sqrt(((b.verts - pos) ** 2).sum(axis=1)) for b in Balls]
    clip = np.array(list(map( lambda i: np.min(i), clip)))
    return np.argsort(clip)[::-1]

