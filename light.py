import numpy as np
import pygame
from math import sqrt

class Light:
    def __init__(self, pos=(0, 0, 0)):
        self.pos = list(pos)


    def update(self, dt, keys):
        if keys[pygame.K_y]: self.pos[1] += dt; print(self.pos) # move up
        elif keys[pygame.K_r]: self.pos[1] -= dt; print(self.pos) # move down

        elif keys[pygame.K_t]: self.pos[2] += dt; print(self.pos) # move foward
        elif keys[pygame.K_g]: self.pos[2] -= dt; print(self.pos) # move backward

        elif keys[pygame.K_h]: self.pos[0] += dt; print(self.pos) # move right
        elif keys[pygame.K_f]: self.pos[0] -= dt; print(self.pos) # move right

        elif keys[pygame.K_o]: self.pos = [0, -7, 0]; print(self.pos)


    def DotProductLight(self, N):
        pos = np.array(self.pos, dtype=np.float16)
        L = sqrt((pos ** 2).sum())
        pos /= L

        N = np.multiply(N, pos)
        return N.sum(axis=1)


    @staticmethod
    def lightPercentage(N):
        return (N + 1) / 2.


    @staticmethod
    def lightColor(colorsF, percentage):
        c = np.copy(colorsF)
        c[..., 0] *= percentage
        c[..., 1] *= percentage
        c[..., 2] *= percentage
        return c.astype(int)
