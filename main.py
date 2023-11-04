# -*- coding: UTF-8 -*-
# GameJam 2023 - Death Is Not The End
# Date: 04-11-2023
# Author: Jörg Angermayer and Paul
# Licence: Freeware
import math

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


class Ghost:
    def __init__(self, name, x, y):
        self.name = name
        self.x = 200
        self.y = 200
        self.img = pygame.image.load("assets/Gost.png")
        self.img = pygame.transform.scale(self.img, (64, 64)) ### orig 32x32
        self.speed = 2.8

    def goLeft(self):
        self.x = self.x - self.speed
    def goRight(self):
        self.x = self.x + self.speed
    def goUp(self):
        self.y = self.y - self.speed
    def goDown(self):
        self.y = self.y + self.speed

class JohnDoe:
    def __init__(self, walls,  name, x, y):
        self.walls = walls
        self.name = name
        self.x = 100
        self.y = 100
        self.prex = 100
        self.prey = 100
        self.img = pygame.image.load("assets/john_doe.png")
        self.img = pygame.transform.scale(self.img, (64, 64))  ### orig 32x32
        self.speed = 2.2
        self.minDistance = 300
        self.minFearDistance = 100
        self.minPanikDistance = 60

    def proofWallCollision(self, colx, coly):
        wallXLimit = 60
        colx = int(colx)
        retVal = 0
        i = 0
        imax = 100
        while i < imax:
            wallX = int(self.walls.obstacles[i].start.x)
            minWallX = int(wallX - wallXLimit)
            maxWallX = int(wallX + wallXLimit)

            minY = int(self.walls.obstacles[i].start.y)
            maxY = int(self.walls.obstacles[i].end.y)

            if colx > minWallX and colx < maxWallX:
                if coly > minY and coly < maxY:
                    retVal = 1

            i = i + 1

        return retVal;

    def geheZuPos(self, inx, iny):
        distanz = math.sqrt(((inx-self.x)*(inx-self.x)) + ((iny-self.y)*(iny-self.y)))
        if distanz < self.minDistance:
            if distanz > self.minFearDistance:
                if inx > self.x:
                    self.prex = self.x + self.speed
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.x = self.x + self.speed
                else:
                    self.prex = self.x - self.speed
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.x = self.x - self.speed

                if iny > self.y:
                    self.prey = self.y + self.speed
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.y = self.y + self.speed
                else:
                    self.prey = self.y - self.speed
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.y = self.y - self.speed

            if distanz < self.minFearDistance:
                if inx > self.x:
                    self.prex = self.x - self.speed
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.x = self.x - self.speed
                else:
                    self.prex = self.x + self.speed
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.x = self.x + self.speed

                if iny > self.y:
                    self.prey = self.y - self.speed
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.y = self.y - self.speed
                else:
                    self.prey = self.y + self.speed
                    if self.proofWallCollision(self.prex , self.prey) == 0:
                        self.y = self.y + self.speed

                if distanz < self.minPanikDistance:
                    self.prex = 100
                    self.prey = 100
                    self.x = 100
                    self.y = 100

def restartGame():
    Level = 1
    player01Highscore = 0


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
        if offsetX < 1500:
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
            offsetX = offsetX + randomX + 100
        x = x + 1

def drawLevelWalls(screen, johnDoO):
    i = 0
    imax = 100
    while i < imax:
        pygame.draw.line(screen, (120, 120, 120), (johnDoO.obstacles[i].start.x, johnDoO.obstacles[i].start.y), (johnDoO.obstacles[i].end.x, johnDoO.obstacles[i].end.y), 10)
        i = i + 1

def main():
    pygame.init()

    screenSize_x = 1600
    screenSize_y = 900
    screen = pygame.display.set_mode((screenSize_x, screenSize_y))

    imgBackground = pygame.image.load("assets/background.png")

    gameover = 0

    # Titel des Fensters setzen, Mauszeiger nicht verstecken und Tastendrücke wiederholt senden.
    pygame.display.set_caption("GameJam2023 - DeathIsNotTheEnd - GhostWork")
    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(1, 30)

    # Clock-Objekt erstellen, das wir benötigen, um die Framerate zu begrenzen.
    clock = pygame.time.Clock()

    johnDoO = Walls()
    createLevelWalls(johnDoO)
    ghostInGame = Ghost("TheGhost",100,100)
    johnDoeInGame = JohnDoe(johnDoO, "JohnDoe", 100, 100)

    running = 1;
    while running:

        clock.tick(30) #30 FPS
        screen.fill((200, 200, 200)) # screen-Surface mit Schwarz (RGB = 0, 0, 0) füllen.
        screen.blit(imgBackground, (0, 0))

        drawLevelWalls(screen, johnDoO)

        for event in pygame.event.get():
            # Exit with Esc
            if event.type == pygame.QUIT:
                running = False

            # Key-Events - key was pressed
            if event.type == pygame.KEYDOWN:
                if gameover == 1:
                    if event.key == pygame.K_RETURN:
                        print("K_return/Reset")
                        restartGame()

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

                if event.key == pygame.K_e:
                    print("Erschrecken")
                    johnDoeInGame.geheZuPos(100, 100)

            #draw
            screen.blit(ghostInGame.img, (ghostInGame.x, ghostInGame.y))
            screen.blit(johnDoeInGame.img, (johnDoeInGame.x, johnDoeInGame.y))


        # Inhalt von screen anzeigen.
            pygame.display.flip()


# Überprüfen, ob dieses Modul als Programm läuft und nicht in einem anderen Modul importiert wird.

if __name__ == '__main__':
    # Unsere Main-Funktion aufrufen.

    main()