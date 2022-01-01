import numpy as np
import pygame
from tools import rotation_y

class Stick:
    def __init__(self, verts):
        self.verts = np.copy(verts)
        self.angle = 0


    def update(self, dt, keys):
        if keys[pygame.K_LEFT]: self.angle += dt / 10 # rotate stick left
        if keys[pygame.K_RIGHT]: self.angle -= dt / 10 # rotate stick right
        if keys[pygame.K_UP]: self.verts[..., 0] += dt  # rotate stick foward
        if keys[pygame.K_DOWN]: self.verts[..., 0] -= dt  # rotate stick backward


    def rotate_stick(self, ballCenter):  
        v = np.array(self.verts)
        v -= ballCenter
        rotMat = rotation_y(self.angle)
        pRot = np.array(list(map(lambda i: np.dot(rotMat, i), v)))
        pRot += ballCenter
        return pRot
        

    def GetStickCenter(self):
        nbrVerts = len(self.verts)
        return self.verts.sum(axis=0) / nbrVerts


    @staticmethod
    def getCenter(verts):
        nbrVerts = len(verts)
        return verts.sum(axis=0) / nbrVerts

    
    