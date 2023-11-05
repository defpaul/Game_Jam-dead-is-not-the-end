# -*- coding: UTF-8 -*-
# GameJam 2023 - Death Is Not The End
# Date: 04-11-2023
# Author: Jörg Angermayer and Paul
# Licence: Freeware
import math
import time

# Pygame-Modul importieren.
import pygame
import random

# Überprüfen, ob die optionalen Text- und Sound-Module geladen werden konnten.
if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
if not pygame.mixer: print('Fehler pygame.mixer Modul konnte nicht geladen werden!')


class Point:
    def __init__(self, x, y):
        self.x = 0
        self.y = 0

class Line:
    def __init__(self, start, end):
        self.start = Point(0,0)
        self.end = Point(0, 0)

class Walls:
    def __init__(self):
        self.obstacles = []
        i = 0
        imax = 100
        while i < imax:
            self.obstacles.append( Line(Point(0, 0), Point(0, 0)) )
            i = i + 1

class AntiGhost:
    def __init__(self, x, y):
        self.x = 300
        self.y = 300
        self.img = pygame.image.load("assets/han.png")
        self.img = pygame.transform.scale(self.img, (64, 64)) ### orig 32x32

class AntiGhostArray:
    def __init__(self):
        self.anti = []
        self.initRandomAntiGhost()

    def initRandomAntiGhost(self):
        i = 0
        imax = 10
        while i < imax:
            x = 200 + (random.random() * 1200)
            y = 100 + (random.random() * 700)
            aghost = AntiGhost(x,y)
            self.anti.append( aghost)
            self.anti[i].x = x
            self.anti[i].y = y
            i = i + 1



class Ghost:
    def __init__(self, inAghost, name, x, y):
        self.aghost = inAghost
        self.name = name
        self.prex = 0
        self.prey = 0
        self.x = x
        self.y = y
        self.distanzeLimit = 60
        self.img = [pygame.image.load("assets/Gost.png"), pygame.image.load("assets/Gost_1.png"),pygame.image.load("assets/Gost.png"), pygame.image.load("assets/Gost_2.png"), ]
        self.img = [pygame.transform.scale(self.img[0], (64, 64)),pygame.transform.scale(self.img[1], (64, 64)),pygame.transform.scale(self.img[2], (64, 64)) ,pygame.transform.scale(self.img[3], (64, 64))] ### orig 32x32
        self.speed = 4
        self.frame_delay = 100
        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()
        self.cunter_time = 0
        self.moved = 0

    def proofGhostWalk(self, inx, iny):
        self.moved = 1
        retVal = 0
        self.moved = 1
        i = 0
        imax = 10
        while i < imax:
            distanz = math.sqrt(((inx - self.aghost.anti[i].x) * (inx - self.aghost.anti[i].x)) + ((iny - self.aghost.anti[i].y) * (iny - self.aghost.anti[i].y)))
            if distanz < self.distanzeLimit:
                retVal = 1
                break
            i = i + 1

        return retVal

    def goLeft(self):
        self.prex = int(self.x - int(self.speed))
        if self.proofGhostWalk(self.prex, self.prey) == 0:
            self.x = self.x - self.speed
    def goRight(self):
        self.prex = int(self.x + int(self.speed))
        if self.proofGhostWalk(self.prex, self.prey) == 0:
            self.x = self.x + self.speed
    def goUp(self):
        self.prey = int(self.y - int(self.speed))
        if self.proofGhostWalk(self.prex, self.prey) == 0:
            self.y = self.y - self.speed
    def goDown(self):
        self.prey = int(self.y + int(self.speed))
        if self.proofGhostWalk(self.prex, self.prey) == 0:
            self.y = self.y + self.speed

    def animations(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_frame_time > self.frame_delay:
            if self.current_frame >= 3:
                self.current_frame = 0
            else:
                self.current_frame = self.current_frame +1
                #print(self.current_frame)
            self.last_frame_time = self.current_time

        #print(f"{self.current_frame}")
        return self.current_frame

    def score(self):
        if self.moved == 1:
            self.cunter_time = self.current_time +1



class JohnDoe:
    def __init__(self, walls,  name, x, y):
        self.walls = walls
        self.name = name
        self.x = x
        self.y = y
        self.prex = 100
        self.prey = 100
        self.img = pygame.image.load("assets/john_doe.png")
        self.img = pygame.transform.scale(self.img, (64, 64))  ### orig 32x32
        self.speed = 2
        self.minDistance = 280
        self.minFearDistance = 90
        self.minPanikDistance = 30

    def proofWallCollision(self, colx, coly):
        wallXLimit = 32
        colx = int(colx)
        coly = int(coly)
        retVal = 0
        i = 0
        imax = 100
        while i < imax:
            wallX = int(self.walls.obstacles[i].start.x-32)
            minWallX = int(wallX - wallXLimit)
            maxWallX = int(wallX + wallXLimit)

            minY = int(self.walls.obstacles[i].start.y+32)
            maxY = int(self.walls.obstacles[i].end.y-32)

            if colx > minWallX and colx < maxWallX:
                if coly > minY and coly < maxY:
                    retVal = 1

            i = i + 1

        return retVal;

    def geheZuPos(self, inx, iny):
        distanz = math.sqrt(((inx-self.x-32)*(inx-self.x-32)) + ((iny-self.y-32)*(iny-self.y-32)))
        if distanz < self.minDistance:
            if distanz >= self.minFearDistance:
                if inx > self.x:
                    prex = int(self.x) + int(self.speed) + 2
                    if self.proofWallCollision(prex , self.prey) == 0:
                        self.x = self.x + int(self.speed)

                if inx < self.x:
                    prex = int(self.x) - int(self.speed) - 2
                    if self.proofWallCollision(prex , self.prey) == 0:
                        self.x = self.x - int(self.speed)

                if iny > self.y:
                    self.prey = int(self.y) + int(self.speed) + 1
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.y = self.y + int(self.speed)
                if iny < self.y:
                    self.prey = int(self.y) - int(self.speed) - 1
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.y = self.y - int(self.speed)

            if distanz < self.minFearDistance:
                if inx > self.x:
                    self.prex = int(self.x) - int(self.speed) - 1
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.x = int(self.x) - int(self.speed)
                else:
                    self.prex = int(self.x) + int(self.speed) + 1
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.x = int(self.x) + int(self.speed)

                if iny > self.y:
                    self.prey = int(self.y) - int(self.speed) - 1
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.y = int(self.y) - int(self.speed)
                else:
                    self.prey = int(self.y) + int(self.speed) + 1
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.y = int(self.y) + int(self.speed)

                if distanz < self.minPanikDistance:
                    self.prex = 100
                    self.prey = 100
                    self.x = 100
                    self.y = 100


def createLevelWalls(johnDoO):
    i = 0
    offsetX = 200
    offsetY = 100
    doorSpace = 100
    rangeYrandom = 200
    randomY = random.random() * rangeYrandom;

    x = 0
    xmax = 16
    while x < xmax:
        if offsetX < 1350:
            randomY = random.random() * rangeYrandom;
            johnDoO.obstacles[i].start.x = offsetX
            johnDoO.obstacles[i].start.y = 0
            johnDoO.obstacles[i].end.x = offsetX
            johnDoO.obstacles[i].end.y = offsetY + randomY
            i = i + 1

            startNewLine = johnDoO.obstacles[i-1].end.y + doorSpace
            if startNewLine < 800:
                johnDoO.obstacles[i].start.x = offsetX
                johnDoO.obstacles[i].start.y = startNewLine
                johnDoO.obstacles[i].end.x = offsetX
                randomY = random.random() * rangeYrandom;
                johnDoO.obstacles[i].end.y = startNewLine + randomY + 40
                i = i + 1

                johnDoO.obstacles[i].start.x = offsetX
                johnDoO.obstacles[i].start.y = johnDoO.obstacles[i-1].end.y + doorSpace
                johnDoO.obstacles[i].end.x = offsetX
                johnDoO.obstacles[i].end.y = 900
            else:
                johnDoO.obstacles[i].start.x = offsetX
                johnDoO.obstacles[i].start.y = startNewLine
                johnDoO.obstacles[i].end.x = offsetX
                johnDoO.obstacles[i].end.y = 900
            i = i + 1

            randomX = random.random() * 180;
            offsetX = offsetX + randomX + 200
        x = x + 1

def drawLevelWalls(screen, johnDoO):
    i = 0
    imax = 100
    while i < imax:
        pygame.draw.line(screen, (120, 120, 120), (johnDoO.obstacles[i].start.x, johnDoO.obstacles[i].start.y), (johnDoO.obstacles[i].end.x, johnDoO.obstacles[i].end.y), 10)
        i = i + 1

def drawLevelAntiGhosts(screen, aghost):
    i = 0
    imax = 10
    while i < imax:
        screen.blit(aghost.anti[i].img, (aghost.anti[i].x, aghost.anti[i].y))
        i = i + 1

class Exit:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.img = pygame.image.load("assets/exit.png")
        self.img = pygame.transform.scale(self.img, (64, 64))
        self.imgwin = pygame.image.load("assets/winn_screan.png")

    def scan(self, johnDoO):
        if self.posx < johnDoO.x +30 and self.posy < johnDoO.y +30 :
            return 1
        else:
            return 0


def main():
    pygame.init()
    screenSize_x = 1600
    screenSize_y = 900
    youwon = 0
    #cunter_display = f"{cunter} s"
    exitcounter = 0
    screen = pygame.display.set_mode((screenSize_x, screenSize_y))
    imgBackground = pygame.image.load("assets/background.png")

    # Titel des Fensters setzen, Mauszeiger nicht verstecken und Tastendrücke wiederholt senden.
    pygame.display.set_caption("GameJam2023 - DeathIsNotTheEnd - GhostWork")
    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(1, 30)

    font = pygame.font.Font(None, 50)
    text_obj = font.render(f"{0} s", True, (255, 255, 255))

    clock = pygame.time.Clock() # Clock-Objekt erstellen, das wir benötigen, um die Framerate zu begrenzen.

    johnDoO = Walls()
    createLevelWalls(johnDoO)
    johnDoeInGame = JohnDoe(johnDoO, "JohnDoe", 100, 100)
    antighost = AntiGhostArray();
    ghostInGame = Ghost(antighost, "TheGhost", 100, 400)
    exit = Exit(1400,600)
    #exit = Exit(100, 400)

    running = 1;
    while running:
        clock.tick(30) #30 FPS
        #screen.fill((200, 200, 200)) # screen-Surface mit Schwarz (RGB = 0, 0, 0) füllen.

        for event in pygame.event.get():
            # Exit with Esc
            if event.type == pygame.QUIT:
               running = False

            # Key-Events - key was pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("K_return/Reset")

                if event.key == pygame.K_SPACE:
                    print("K_space")

                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

                if event.key == pygame.K_LEFT:
                    ghostInGame.goLeft()

                if event.key == pygame.K_RIGHT:
                    ghostInGame.goRight()

                if event.key == pygame.K_UP:
                    ghostInGame.goUp()

                if event.key == pygame.K_DOWN:
                    ghostInGame.goDown()

                if event.key == pygame.K_k:
                    johnDoeInGame.geheZuPos(ghostInGame.x, ghostInGame.y)
                    ghostInGame.moved = 1

                if event.key == pygame.K_e:
                    print("Erschrecken")
                    johnDoeInGame.geheZuPos(100, 100)

        if ghostInGame.moved == 1:
            text_obj = font.render(f"{round(ghostInGame.cunter_time /300, 2)} s", True, (255, 255, 255))



        youwon = exit.scan(johnDoeInGame)
        frame = ghostInGame.animations()

        #draw
        screen.blit(imgBackground, (0, 0))
        drawLevelWalls(screen, johnDoO)
        drawLevelAntiGhosts(screen, antighost)
        screen.blit(exit.img, (exit.posx, exit.posy))
        #pygame.draw.circle(screen, (200, 200, 255), (ghostInGame.x + 32, ghostInGame.y + 32), johnDoeInGame.minDistance,4)
        screen.blit(ghostInGame.img[frame], (ghostInGame.x, ghostInGame.y))
        screen.blit(johnDoeInGame.img, (johnDoeInGame.x, johnDoeInGame.y))
        screen.blit(text_obj, (800, 50))


        if youwon == 1:
            exitcounter =  exitcounter + 1
            ghostInGame.moved = 0
            screen.blit(exit.imgwin, (0, 0))
            if exitcounter > 60:
                createLevelWalls(johnDoO)
                johnDoeInGame.x = 100
                johnDoeInGame.y = 100
                ghostInGame.x = 100
                ghostInGame.y = 400
                ghostInGame.cunter_time = 0


        # Inhalt von screen anzeigen.
        ghostInGame.score()
        if ghostInGame.moved == 1:
            text_obj = font.render(f"{round(ghostInGame.cunter_time /300, 2)} s", True, (255, 255, 255))
        pygame.display.flip()

if __name__ == '__main__':
    main()