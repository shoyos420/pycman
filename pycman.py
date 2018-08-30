
#libreria pygame
import pygame, sys, os, random, time
from pygame.locals import *

#direccionamos nuestra carpeta para mejorar el orden
SCRIPT_PATH=sys.path[0]

clock = pygame.time.Clock()
pygame.init()

#definicion de nuestra ventana y pantalla
window = pygame.display.set_mode((1, 1))
pygame.display.set_caption("Pycman")
screen = pygame.display.get_surface()
##background = pygame.Surface(screen.get_size())
##background = background.convert()
##background.fill((250, 250, 250))


##______________/ Clase Pacman \____________________##


#primera definicion para el manejo de pacman en la ventana
#primeras etapas para graficar en ventana




class pacman ():

    def __init__ (self):
        self.x = 0
        self.y = 0

        self.velx = 0
        self.vely = 0

        self.speed=1

        self.animFrame=1



        self.anim_pacmanL = {}
        self.anim_pacmanR = {}
        self.anim_pacmanU = {}
        self.anim_pacmanD = {}
        self.anim_pacmanS = {}
        self.anim_pacmanCurrent = {}



        #generamos un array de nuestas imagenes
        for i in range(1, 9, 1):
            self.anim_pacmanL[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-l " + str(i) + ".gif")).convert()
            self.anim_pacmanR[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-r " + str(i) + ".gif")).convert()
            self.anim_pacmanU[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-u " + str(i) + ".gif")).convert()
            self.anim_pacmanD[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-d " + str(i) + ".gif")).convert()
            self.anim_pacmanS[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman.gif")).convert()




    def Draw (self):

        if self.velx > 0:
            self.anim_pacmanCurrent = self.anim_pacmanR
        elif self.velx < 0:
            self.anim_pacmanCurrent = self.anim_pacmanL
        elif self.vely > 0:
            self.anim_pacmanCurrent = self.anim_pacmanD
        elif self.vely < 0:
            self.anim_pacmanCurrent = self.anim_pacmanU
        else :
            self.anim_pacmanCurrent = self.anim_pacmanR


        screen.blit (self.anim_pacmanCurrent[ self.animFrame ], (self.x, self.y ))
        #screen.blit (self.anim_pacmanD[3], (self.x,self.y))

        if not self.velx == 0 or not self.vely == 0:
            # solo anima la boca cuando pacman se mueva
            self.animFrame += 1

        if self.animFrame == 9:
            # termina la animacion e inicia nuevamente
            self.animFrame = 1

    def Move (self):
        self.x += self.velx
        self.y += self.vely


#______________/ entradas \____________________________

def CheckInputs():


    if pygame.key.get_pressed()[ pygame.K_RIGHT ] :

        player.velx = player.speed
        player.vely = 0

    elif pygame.key.get_pressed()[ pygame.K_LEFT ] :

        player.velx = -player.speed
        player.vely = 0

    elif pygame.key.get_pressed()[ pygame.K_DOWN ] :
        player.velx = 0
        player.vely = player.speed

    elif pygame.key.get_pressed()[ pygame.K_UP ] :

        player.velx = 0
        player.vely = -player.speed


    if pygame.key.get_pressed()[ pygame.K_ESCAPE ]:
        sys.exit(0)





#______________/ game init \____________________________

player = pacman()

def main():


    screenSize = (400, 500)
    window = pygame.display.set_mode( screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE )





    pygame.display.flip()


    while 1:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                return






        player.Draw()
        player.Move()
        pygame.display.flip()
        CheckInputs()
        clock.tick (60)





if __name__ == '__main__': main()
