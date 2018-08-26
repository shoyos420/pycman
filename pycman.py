
#libreria pygame
import pygame, sys, os, random
from pygame.locals import *

#direccionamos nuestra carpeta para mejorar el orden
SCRIPT_PATH=sys.path[0]

clock = pygame.time.Clock()
pygame.init()

#definicion de nuestra ventana y pantalla
window = pygame.display.set_mode((1, 1))
pygame.display.set_caption("Pycman")
screen = pygame.display.get_surface()


##______________/ Clase Pacman \____________________##


#primera definicion para el manejo de pacman en la ventana
#primeras etapas para graficar en ventana



class pacman ():

    def __init__ (self):
        self.x = 0
        self.y = 0



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

        screen.blit (self.anim_pacmanD[3], (self.x+300,self.y+200))





#______________/ game init \____________________________

screenSize = (400, 500)
window = pygame.display.set_mode( screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE )
player = pacman()

while 1:

    event=pygame.event.wait()
    player.Draw()
    pygame.display.flip()
    if event == pygame.QUIT:
        break


pygame.quit()


clock.tick (60)
