import pygame
from tools import rotation
from math import pi

class Camera:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.rel
            x /= 200 # mouse sensor
            y /= 200 # mouse sensor
            self.rot[0] += y; self.rot[1] -= x

    def update(self, dt, keys): # camera movements

        if keys[pygame.K_LSHIFT]: self.pos[1] += dt # move up
        if keys[pygame.K_SPACE]: self.pos[1] -= dt # move down

        if keys[pygame.K_z]: # move foward
            forward = rotation(-self.rot[0], -self.rot[1], -self.rot[2], [0, 0, 1])
            self.pos[0] += dt * forward[0]
            self.pos[1] += dt * forward[1]
            self.pos[2] += dt * forward[2]
            
        if keys[pygame.K_s]:  # move backward
            backward = rotation(-self.rot[0], -self.rot[1], -self.rot[2], [0, 0, 1])
            self.pos[0] -= dt * backward[0]
            self.pos[1] -= dt * backward[1]
            self.pos[2] -= dt * backward[2]

        if keys[pygame.K_d]: # move right
            left = rotation(-self.rot[0], -self.rot[1], -self.rot[2], [1, 0, 0])
            self.pos[0] += dt * left[0]
            self.pos[1] += dt * left[1]
            self.pos[2] += dt * left[2]

        if keys[pygame.K_q]: # move left
            right = rotation(-self.rot[0], -self.rot[1], -self.rot[2], [1, 0, 0])
            self.pos[0] -= dt * right[0]
            self.pos[1] -= dt * right[1]
            self.pos[2] -= dt * right[2]

        if keys[pygame.K_w]: self.rot[2] -= dt /10 # rotate the right side
        if keys[pygame.K_x]: self.rot[2] += dt /10 # rotate the left side
        if keys[pygame.K_5]: self.rot[0] = pi / 2; self.pos = [0, -12, 0]