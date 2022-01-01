import numpy as np
import pygame
from math import cos, sin

def projection_mat(alpha, beta, f, cx, cy):
    return np.array([
        [f * alpha, 0, cx],
        [0, f * beta, cy],
        [0, 0, 1]
    ])

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def rotation_x(angle_x):
    return np.array([
        [1, 0, 0],
        [0, cos(angle_x), - sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)]
    ])

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def rotation_y(angle_y):
    return np.array([
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [- sin(angle_y), 0, cos(angle_y)]
    ])

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def rotation_z(angle_z):
    return np.array([
        [cos(angle_z), - sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1]
    ])

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def rotationn(a, b, s):
    Ca, Cb, Cs = cos(a), cos(b), cos(s)
    Sa, Sb, Ss = sin(a), sin(b), sin(s)
    return np.array([
        [Ca * Cb,      Ca * Sb * Ss - Sa * Cs,     Ca * Sb * Cs + Sa * Ss],
        [Sa * Cb,      Sa * Sb * Ss + Ca * Cs,     Sa * Sb * Cs - Ca * Ss],
        [-Sb,          Cb * Ss,                    Cb * Cs]
    ])

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def rotation2d(point, angle):
    mat = np.array([
        [cos(angle), -sin(angle)],
        [sin(angle), cos(angle)]
        ])
    return np.dot(mat, point)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def rot_mat(angle_x, angle_y, angle_z):
    return np.matmul(np.matmul(rotation_x(angle_x), rotation_y(angle_y)), rotation_z(angle_z))

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def rotation(angle_x, angle_y, angle_z, point):
    return np.matmul(np.matmul(np.matmul(rotation_x(angle_x), rotation_y(angle_y)), rotation_z(angle_z)), point)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def projection(points, f: int, alpha :int, beta :int, cx: int, cy: int, rot: list, pos: list):
    points_3D = np.array(points)
    points_3D[:, 0] -= pos[0]
    points_3D[:, 1] -= pos[1]
    points_3D[:, 2] -= pos[2]
    rotation = rot_mat(*rot)
    for i in range(len(points_3D)): points_3D[i] = np.dot(rotation, points_3D[i])
    projected_points = np.array(points_3D)
    projected_points[..., 0] /= points_3D[..., 2]
    projected_points[..., 1] /= points_3D[..., 2]
    projected_points[..., 2] /= points_3D[..., 2]
    for i in range(len(projected_points)): projected_points[i] = np.dot(projection_mat(alpha, beta, f, cx, cy), projected_points[i])
    return projected_points, points_3D

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def connect_points(screen, x , y, points):
    pygame.draw.line(screen, (255, 255, 255), (points[x][0], points[x][1]), (points[y][0], points[y][1]))

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def draw_polygon(screen, color, p, points):
    p1, p2, p3 = p
    pygame.draw.polygon(screen, color, [(points[p1][0], points[p1][1]), (points[p2][0], points[p2][1]), (points[p3][0], points[p3][1])])

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def ball_raduis(projected_ball):
    x_mx = np.max(projected_ball[..., 0])
    x_mn = np.min(projected_ball[..., 0])
    y_mx = np.max(projected_ball[..., 1])
    y_mn = np.min(projected_ball[..., 1])
    z_mx = np.max(projected_ball[..., 2])
    z_mn = np.min(projected_ball[..., 2])
    center = np.array([(x_mx + x_mn) / 2., (y_mx + y_mn) / 2., (z_mx + z_mn) / 2.])
    raduis = (z_mx - z_mn) / 2.
    return center, raduis

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


