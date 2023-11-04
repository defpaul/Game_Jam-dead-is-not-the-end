# -*- coding: UTF-8 -*-
# GameJam 2023 - Death Is Not The End
# Date: 04-11-2023
# Author: Jörg Angermayer and Paul
# Licence: Freeware


# Pygame-Modul importieren.
import pygame
import random

# Überprüfen, ob die optionalen Text- und Sound-Module geladen werden konnten.
if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
if not pygame.mixer: print('Fehler pygame.mixer Modul konnte nicht geladen werden!')

class Ghost:
    def __init__(self, name, x, y):
        self.name = name
        self.x = 600
        self.y = 300
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
    def __init__(self, name, x, y):
        self.name = name
        self.x = 100
        self.y = 100
        self.img = pygame.image.load("assets/john_doe.png")
        self.img = pygame.transform.scale(self.img, (64, 64))  ### orig 32x32
        self.speed = 2.2

    def geheZuPos(self, inx, iny):
        if inx > self.x:
            self.x = self.x + self.speed
        else:
            self.x = self.x - self.speed

        if iny > self.y:
            self.y = self.y + self.speed
        else:
            self.y = self.y - self.speed


def restartGame():
    gameover = 0
    Level = 1
    player01Highscore = 0
    #imgKoralle01 = pygame.image.load("pic/koralle02.png")

def reduceRed(img):
    gameover = 1
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            pixelColor = img.get_at((x, y))
            if pixelColor.r > 10:
                gameover = 0
                pixelColor.r = pixelColor.r - 10
            img.set_at((x, y), pixelColor)
    return gameover

def main():
    pygame.init()
    ghostInGame = Ghost("TheGhost",100,100);
    johnDoeInGame = JohnDoe("JohnDoe", 100, 100);

    screenSize_x = 1600
    screenSize_y = 900
    screen = pygame.display.set_mode((screenSize_x, screenSize_y))

    gameover = 0

    # Titel des Fensters setzen, Mauszeiger nicht verstecken und Tastendrücke wiederholt senden.
    pygame.display.set_caption("GameJam2023 - DeathIsNotTheEnd - GhostWork")
    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(1, 30)

    # Clock-Objekt erstellen, das wir benötigen, um die Framerate zu begrenzen.
    clock = pygame.time.Clock()

    running = 1;
    while running:

        clock.tick(30) #30 FPS
        screen.fill((200, 200, 200)) # screen-Surface mit Schwarz (RGB = 0, 0, 0) füllen.

        for event in pygame.event.get():
            #print("imgTrash01Pos_y:",imgTrash01Pos_y)
            #print("playerpositionAbs_y: ",playerpositionAbs_y, " --- imgTrash01Pos_y: ",imgTrash01Pos_y)
            #print("imgTrash01PosAbs_y:",imgTrash01PosAbs_y," --- playerpositionAbs_y:",playerpositionAbs_y)

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
                    print("K_Left")
                    ghostInGame.goLeft()

                if event.key == pygame.K_RIGHT:
                    print("K_Right")
                    ghostInGame.goRight()

                if event.key == pygame.K_UP:
                    print("K_Up")
                    ghostInGame.goUp()

                if event.key == pygame.K_DOWN:
                    print("K_Down")
                    ghostInGame.goDown()

                if event.key == pygame.K_k:
                    print("klopfKlop")
                    johnDoeInGame.geheZuPos(ghostInGame.x, ghostInGame.y)

                if event.key == pygame.K_e:
                    print("Erschrecken")

            #draw
            screen.blit(ghostInGame.img, (ghostInGame.x, ghostInGame.y))
            screen.blit(johnDoeInGame.img, (johnDoeInGame.x, johnDoeInGame.y))


        # Inhalt von screen anzeigen.
            pygame.display.flip()


# Überprüfen, ob dieses Modul als Programm läuft und nicht in einem anderen Modul importiert wird.

if __name__ == '__main__':
    # Unsere Main-Funktion aufrufen.

    main()