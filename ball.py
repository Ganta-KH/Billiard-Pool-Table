from math import pi, sqrt, cos, sin, atan
from tools import ball_raduis
import pygame

class Ball:
    def __init__(self, verts: list, faces: list, center: list, radius: float, color: list, number: int):
        self.verts = verts
        self.faces = faces
        self.center = center
        self.radius = radius
        self.color = color
        self.number = number
        self.power = 0
        self.angle = None
        self.turnUP, self.turnDown, self.turnRight, self.turnLeft = 1, 1, 1, 1

    def update(self, dt ,keys, minW, maxW, minH, maxH):
        if keys[pygame.K_RIGHT]: 
            if (self.center[0] + dt / 5 + self.radius) < maxW: 
                self.verts[..., 0] += dt / 5
                self.center[0] += dt / 5

        if keys[pygame.K_LEFT]:
            if (self.center[0] - dt / 5 - self.radius) > minW: 
                self.verts[..., 0] -= dt / 5
                self.center[0] -= dt / 5

        if keys[pygame.K_UP]:
            if (self.center[2] + dt / 5 + self.radius) < maxH: 
                self.verts[..., 2] += dt / 5
                self.center[2] += dt / 5
            
        if keys[pygame.K_DOWN]:
            if (self.center[2] - dt / 5 - self.radius) > minH: 
                self.verts[..., 2] -= dt / 5
                self.center[2] -= dt / 5

    def findAngle(self, pos_2):
        try: angle = atan( (self.center[2] - pos_2[2]) / (self.center[0] - pos_2[0]) )
        except:
            if pos_2[2] < self.center[2] and pos_2[0] == self.center[0]: angle = pi / 2 # up
            elif pos_2[2] > self.center[2] and pos_2[0] == self.center[0]: angle = (3 * pi) / 2 # down

        if pos_2[2] == self.center[2] and pos_2[0] > self.center[0]: angle = 2 * pi # right
        elif pos_2[2] == self.center[2] and pos_2[0] < self.center[0]: angle = pi # left
        elif pos_2[2] < self.center[2] and pos_2[0] > self.center[0]: angle = abs(angle) # up right
        elif pos_2[2] < self.center[2] and pos_2[0] < self.center[0]: angle = pi - angle # up left
        elif pos_2[2] > self.center[2] and pos_2[0] < self.center[0]: angle = pi + abs(angle) # down left
        elif pos_2[2] > self.center[2] and pos_2[0] > self.center[0]: angle = (pi * 2) - angle # down right: 

        return angle


    def whiteBallShoot(self, pos_2):
        self.turnUP, self.turnDown, self.turnRight, self.turnLeft = 1, 1, 1, 1
        self.power = sqrt( (self.center[0] - pos_2[0]) ** 2 + (self.center[2] - pos_2[2]) ** 2 ) / 5.
        self.angle = (self.findAngle(pos_2) - pi) * -1


    def ballPath(self, time):
        self.velx = cos(self.angle) * self.power
        self.vely = sin(self.angle) * self.power

        distX = self.velx * time
        distY = self.vely * time

        return distX , distY


    def ballMovment(self, shoot, minW, maxW, minH, maxH):     
        if (minW + self.radius < self.center[0] < maxW - self.radius) and (minH + self.radius < self.center[2] < maxH - self.radius) and self.power > .01:
            time = .5
            self.power *= .97
            nextX, nextZ = self.ballPath(time)
            self.verts[..., 0] += nextX
            self.verts[..., 2] += nextZ
            self.center[0] += nextX
            self.center[2] += nextZ
        else:
            if self.power <= .01:
                self.power = 0
                self.angle = None
                shoot = False

            if self.center[2] >= maxH - self.radius:
                self.turnUP *= -1
                self.angle = self.findAngle([self.center[0] + self.velx, self.center[1], self.center[2] + (self.vely * self.turnUP * self.turnDown)])
                self.verts[..., 2] -= self.radius
                self.center[2] -= self.radius #self.center, _ = ball_raduis(self.verts)
            
            elif self.center[0] >= maxW - self.radius:
                self.turnLeft *= -1
                self.angle = self.findAngle([self.center[0] + (self.velx * self.turnLeft * self.turnRight * -1), self.center[1], self.center[2] + self.vely]) * -1
                self.verts[..., 0] -= self.radius
                self.center[0] -= self.radius #self.center, _ = ball_raduis(self.verts)
            
            elif self.center[0] <= minW + self.radius:
                self.turnRight *= -1
                self.angle = self.findAngle([self.center[0] + (self.velx * self.turnLeft * self.turnRight * -1), self.center[1], self.center[2] + self.vely]) * -1
                self.verts[..., 0] += self.radius
                self.center[0] += self.radius #self.center, _ = ball_raduis(self.verts)
            
            elif self.center[2] <= minH + self.radius:
                self.turnDown *= -1
                self.angle = self.findAngle([self.center[0] + self.velx, self.center[1], self.center[2] + (self.vely * self.turnUP * self.turnDown)])
                self.verts[..., 2] += self.radius
                self.center[2] += self.radius #self.center, _ = ball_raduis(self.verts)
        
        return shoot


    def collisionDetections(self, balls):
        dist = sqrt( (self.center[0] - balls.center[0]) ** 2 + (self.center[2] - balls.center[2]) ** 2 )
        return True if dist < self.radius * 2 else False

