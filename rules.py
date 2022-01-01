from math import sqrt, pi

def getInHole(Balls, Holes):
    for count, ball in enumerate(Balls):
        for hole in Holes:
            dist = sqrt( (hole[0] - ball.center[0]) ** 2  + (hole[2] - ball.center[2]) ** 2 )
            if dist <= ball.radius*2:
                if count == 0: 
                    return True
                else: Balls.remove(ball)


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def allCollision(Balls):
    for count, ball in enumerate(Balls):
        for i in range(count + 1, len(Balls)):
            if ball.collisionDetections(Balls[i]):
                if ball.power >= Balls[i].power: Balls[i].power = ball.power * 0.9
                else: ball.power = Balls[i].power * 0.9
                ball.angle = (ball.findAngle(Balls[i].center) - pi) * -1
                Balls[i].angle = (Balls[i].findAngle(ball.center) - pi) * -1