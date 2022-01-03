import sys, os

from tools import projection, rotation, connect_points, draw_polygon
from const import *
from clip import clipping, CrossProduct, DotProduct, Zfarrr
from rules import getInHole, allCollision

def main():
    
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.event.get()
    pygame.mouse.get_rel()

    cam = False
    line = True
    shoot = False
    move = True
    start = True
    Cross_ProductB = np.zeros((nbrBalls, nbrFacesInBall, 3))
    projected_balls = np.zeros((nbrBalls, nbrPointsInBall, 3))

    while True:
        dt = clock.tick() / 100.
        pygame.display.set_caption('3D Billiard Pool - FPS: %.2f' % clock.get_fps())


        if shoot:
            allCollision(Balls)
            move = getInHole(Balls, centersH)
            if all([ball.ballMovment(shoot, minW, maxW, minH, maxH) == False for ball in Balls]): 
                shoot = False
                distZ = WhiteBall.center[2] - stick.GetStickCenter()[2]
                stick.verts[..., 2] += distZ
        elif not shoot and move:
            WhiteBall.verts = pointsB[0: nbrPointsInBall]
 
        
        r = rotation(camera.rot[0], camera.rot[1], camera.rot[2], [0, 0, 1])[2]

        # Table
        projected_table, table_3D = projection(pointsT, f, alpha, beta, cx, cy, camera.rot, camera.pos)
        Cross_ProductT = CrossProduct(table_3D, facesT)
        Dot_ProductT = DotProduct(table_3D, facesT, camera, Cross_ProductT)
        clipT = clipping(projected_table, table_3D, Dot_ProductT, facesT, r, W, H)

        if len(clipT) != 0: Dot_ProductT = Dot_ProductT[clipT]
        else: Dot_ProductT = np.array([])

        Dot_ProductT = Dot_ProductT[::-1]

        # Balls
        Dot_ProductB = []
        for i in range(len(Balls)):
            pballs, b3D = projection(Balls[i].verts, f, alpha, beta, cx, cy, camera.rot, camera.pos)
            Cross_ProductB[i] = CrossProduct(b3D, Balls[i].faces)
            Dot_ProductB += [DotProduct(b3D, Balls[i].faces, camera, Cross_ProductB[i])]
            clipB = clipping(pballs, b3D, Dot_ProductB[i], Balls[i].faces, r, W, H)[::-1]
            if len(clipB) != 0: Dot_ProductB[i] = Dot_ProductB[i][clipB]
            else: Dot_ProductB[i] = np.array([])

            projected_balls[i] = pballs

        ZclipB = Zfarrr(Balls, camera.pos)

        # Stick
        if not shoot and not move:
            pS = stick.rotate_stick(WhiteBall.center)
            projected_stick, stick_3D = projection(pS, f, alpha, beta, cx, cy, camera.rot, camera.pos)
            Cross_ProductS = CrossProduct(stick_3D, facesS)
            Dot_ProductS = DotProduct(stick_3D, facesS, camera, Cross_ProductS)
            clipS = clipping(projected_stick, stick_3D, Dot_ProductS, facesS, r, W, H)

            if len(clipS) != 0: Dot_ProductS = Dot_ProductS[clipS]
            else: Dot_ProductS = np.array([])

            Dot_ProductS = Dot_ProductS[::-1]



        # draw
        if not line:
            screen.fill((0, 0, 0))

            # Table
            if len(Dot_ProductT) != 0:
                for face in facesT[Dot_ProductT]:
                    for edge in range(0, 3):
                        connect_points(screen, face[edge-1], face[edge], projected_table)

            # Balls
            for i in ZclipB:
                if len(Dot_ProductB[i]) != 0:
                    for face in facesB[Dot_ProductB[i]]:
                        for edge in range(0, 3):
                            connect_points(screen, face[edge-1], face[edge], projected_balls[i])

            # Stick
            if not shoot and not move and len(Dot_ProductS) != 0:
                for face in facesS[Dot_ProductS]:
                    for edge in range(0, 3):
                        connect_points(screen, face[edge-1], face[edge], projected_stick)

        else:
            screen.fill((9, 112, 147)) # (128,128,255) # (18, 91, 132) # (39, 112, 147)

            # Table
            Dot_Product_Light = light.DotProductLight(Cross_ProductT)
            light_Percentage = light.lightPercentage(Dot_Product_Light)
            colorsFacesT = light.lightColor(colorsFT, light_Percentage)
            for face in Dot_ProductT:
                draw_polygon(screen, colorsFacesT[face], facesT[face], projected_table)

            # Balls
            for i in ZclipB:
                Dot_Product_Light = light.DotProductLight(Cross_ProductB[i])
                light_Percentage = light.lightPercentage(Dot_Product_Light)
                colorsFacesB = light.lightColor(Balls[i].color, light_Percentage)
                for face in Dot_ProductB[i]:
                    draw_polygon(screen, colorsFacesB[face], facesB[face], projected_balls[i])

            # Stick
            if not shoot and not move:
                Dot_Product_Light = light.DotProductLight(Cross_ProductS)
                light_Percentage = light.lightPercentage(Dot_Product_Light)
                colorsFacesS = light.lightColor(colorsFS, light_Percentage)
                for face in Dot_ProductS:
                    draw_polygon(screen, colorsFacesS[face], facesS[face], projected_stick)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit; sys.exit()
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_a: # shoot the white ball
                    if not move:
                        stickcenter = stick.getCenter(pS)
                        WhiteBall.whiteBallShoot(stickcenter)
                        shoot = True
                        stick.angle = 0
                        stick.verts = np.array(pointsS)

                if event.key == pygame.K_e: # move the white ball
                    move = False
                    start = False
                    distZ = WhiteBall.center[2] - stick.GetStickCenter()[2]
                    stick.verts[..., 2] += distZ

                if event.key == pygame.K_ESCAPE: pygame.quit; sys.exit()
                if event.key == pygame.K_c: # type c to rotate with mouse
                    if cam: # start camera control
                        pygame.mouse.set_visible(1)
                        pygame.event.set_grab(0)
                        cam = False
                    else: # stop camera control
                        pygame.mouse.set_visible(0)
                        pygame.event.set_grab(1)
                        cam = True 
                
                if event.key == pygame.K_l: # type L to see a different view
                    if line: line = False
                    else: line = True   
            if cam: camera.events(event)

        keys = pygame.key.get_pressed()
        if cam: camera.update(dt, keys)
        
        light.update(dt, keys)

        if not move and not start: stick.update(dt, keys)
        elif move and not start: Balls[0].update(dt, keys, minW, maxW, minH, maxH)
        elif start:  Balls[0].update(dt, keys, minW, Wstart, minH, maxH)

        pygame.display.flip()

if __name__ == '__main__':
    main()