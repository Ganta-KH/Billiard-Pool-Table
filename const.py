from camera import Camera
from ball import *
from light import Light
from readObj import get_verts
import pygame
from stick import Stick
from tools import ball_raduis
import numpy as np

W, H = 1000, 600

cx, cy = W//2, H//2
f, alpha, beta = 600, 1, 1

pointsT, facesT, colorsT, facesNbrT = get_verts('assets/pool.obj')
pointsB, facesB, colorsB, facesNbrB = get_verts('assets/balls.obj')
pointsS, facesS, colorsS, facesNbrS = get_verts('assets/stick.obj')
pointsH, _, _, _ = get_verts('assets/holles.obj')
colorsFT = np.zeros_like(facesT, dtype=np.float16)
colorsFB = np.zeros_like(facesB, dtype=np.float16)
colorsFS = np.zeros_like(facesS, dtype=np.float16)
facesT = np.fliplr(facesT)
facesB = np.fliplr(facesB)
facesS = np.fliplr(facesS)

# color table faces
for i in range(1, len(facesNbrT)):
    colorsFT[facesNbrT[i-1] : facesNbrT[i]] = colorsT[i-1]

# color balls faces
for i in range(1, len(facesNbrB)):
    colorsFB[facesNbrB[i-1] : facesNbrB[i]] = colorsB[i-1]

# color stick faces
for i in range(1, len(facesNbrS)):
    colorsFS[facesNbrS[i-1] : facesNbrS[i]] = colorsS[i-1]

nbrBalls = len(facesNbrB) - 1
ballsPointsPos = np.linspace(0, pointsB.shape[0], nbrBalls + 1).astype(int)

centers, radiuss = np.zeros((nbrBalls,3)), np.zeros(nbrBalls)

for i in range(1, nbrBalls+1):
    center, radius = ball_raduis(pointsB[ballsPointsPos[i-1] : ballsPointsPos[i]])
    centers[i-1] = center
    radiuss[i-1] = radius

nbrPointsInBall = int(len(pointsB) / nbrBalls)
nbrFacesInBall = int(len(facesB) / nbrBalls)

pB = np.array(pointsB.reshape((nbrBalls, nbrPointsInBall, 3)))
fB = facesB.reshape((nbrBalls, nbrFacesInBall, 3)) % nbrPointsInBall
Balls = [Ball(pB[0], fB[0], centers[0], radiuss[0], colorsFB[0 : 48], 0),
         Ball(pB[1], fB[1], centers[1], radiuss[1], colorsFB[48 : 48 * 2], 3),
         Ball(pB[2], fB[2], centers[2], radiuss[2], colorsFB[48 * 2 : 48 * 3], 12),
         Ball(pB[3], fB[3], centers[3], radiuss[3], colorsFB[48 * 3: 48 * 4], 5),
         Ball(pB[4], fB[4], centers[4], radiuss[4], colorsFB[48 * 4 : 48 * 5], 10),
         Ball(pB[5], fB[5], centers[5], radiuss[5], colorsFB[48 * 5 : 48 * 6], 14),
         Ball(pB[6], fB[6], centers[6], radiuss[6], colorsFB[48 * 6 : 48 * 7], 8),
         Ball(pB[7], fB[7], centers[7], radiuss[7], colorsFB[48 * 7 : 48 * 8], 15),
         Ball(pB[8], fB[8], centers[8], radiuss[8], colorsFB[48 * 8 : 48 * 9], 4),
         Ball(pB[9], fB[9], centers[9], radiuss[9], colorsFB[48 * 9 : 48 * 10], 1),
         Ball(pB[10], fB[10], centers[10], radiuss[10], colorsFB[48 * 10 : 48 * 11], 9),
         Ball(pB[11], fB[11], centers[11], radiuss[11], colorsFB[48 * 11 : 48 * 12], 13),
         Ball(pB[12], fB[12], centers[12], radiuss[12], colorsFB[48 * 12 : 48 * 13], 2),
         Ball(pB[13], fB[13], centers[13], radiuss[13], colorsFB[48 * 13 : 48 * 14], 7),
         Ball(pB[14], fB[14], centers[14], radiuss[14], colorsFB[48 * 14 : 48 * 15], 6),
         Ball(pB[15], fB[15], centers[15], radiuss[15], colorsFB[48 * 15 : 48 * 16], 11)]

WhiteBall = Balls[0]


fT = facesT[facesNbrT[2]: facesNbrT[3]]
fT = fT.flatten()
unique = np.unique(fT)

# get wall value
Xs = pointsT[unique, 0]
Xs = np.unique(Xs)
Zs = pointsT[unique, 2]
Zs = np.unique(Zs)

minW = Xs[1]
maxW = Xs[-2]
Wstart = minW + maxW / 2

minH = Zs[1]
maxH = Zs[-2]

# pygame value
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

# object
camera = Camera((0, -3, -17))
light = Light((0,-7, 0))
stick = Stick(pointsS)

# Holles position
posHolles = np.linspace(0, pointsH.shape[0], 7).astype(int)
centersH, radiusH = [], []
for i in range(1, 7):
    center, radius = ball_raduis(pointsH[posHolles[i-1] : posHolles[i]])
    centersH.append(center)
    radiusH.append(radius)







