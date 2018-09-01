
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
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))


##______________/ Clase Pacman \____________________##


#primera definicion para el manejo de pacman en la ventana
#primeras etapas para graficar en ventana

class Character (object):
    def __init__ (self):
        '''in - (self)'''
        self.surface = None
        self.rect = None
        self.speed = None
        self.velx = None
        self.vely = None
        self.aux=None
        #self.x= None
        #sef.y= None

    def canMove (self, walls):

        rectTest = self.rect

        if self.velx > 0:
            rectTest = self.rect.move ((self.speed, 0))
        elif self.velx < 0:
            rectTest = self.rect.move ((-self.speed, 0))
        elif self.vely > 0:
            rectTest = self.rect.move ((0, self.speed))
        elif self.vely < 0:
            rectTest = self.rect.move ((0, -self.speed))


        #for wall in walls:
        #    if wall.colliderect (rectTest):
        #        if self.aux == 0:
        #            print ("cant")
        #            self.aux+= 1
        #        return False
        self.aux=0
        return True

    def Move (self):



        self.rect.top += self.vely
        self.rect.left += self.velx




class pacman (Character):

    def __init__ (self):
        #self.x = 160
        #self.y = 240

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

        self.rect=self.anim_pacmanL[1].get_rect ()
        self.rect.top=240
        self.rect.left=160


    def Draw (self):

        screen.fill((0,0,0))
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


        screen.blit (self.anim_pacmanCurrent[ self.animFrame ], (self.rect.left, self.rect.top ))
        #screen.blit (self.anim_pacmanD[3], (self.x,self.y))

        if not self.velx == 0 or not self.vely == 0:
            # solo anima la boca cuando pacman se mueva
            self.animFrame += 1

        if self.animFrame == 9:
            # termina la animacion e inicia nuevamente
            self.animFrame = 1






class map():
    def __init__ (self):
        self.drawx=0
        self.drawy=0
        self.wall= pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall.gif")).convert()
        self.wallList=[]









    def draw(self, lvl):

        #screen.fill((0,0,0))

        file = open(os.path.join(SCRIPT_PATH,"res","levels",str(lvl) + ".txt"), 'r')

        for line in file:
            self.drawx=0
            for caracter in line:
                if caracter == '#':
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-straight-horiz.gif")).convert()
                    screen.blit (self.wall, (self.drawx, self.drawy ))
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (16, 16)))
                if caracter == '$':
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-straight-vert.gif")).convert()
                    screen.blit (self.wall, (self.drawx, self.drawy ))
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (16, 16)))
                if caracter == '1' or caracter == '2' or caracter =='3' or caracter == '4' :
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-edge" + caracter + ".gif")).convert()
                    screen.blit (self.wall, (self.drawx, self.drawy ))
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (16, 16)))
                self.drawx+=16
            self.drawy+=16

        self.drawy=0
        self.drawx=0


    def walls(self,lvl):

        file = open(os.path.join(SCRIPT_PATH,"res","levels",str(lvl) + ".txt"), 'r')

        for line in file:
            self.drawx=0
            for caracter in line:
                if caracter == '#':
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (16, 16)))
                if caracter == '$':
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (16, 16)))
                if caracter == '1' or caracter == '2' or caracter =='3' or caracter == '4' :
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (16, 16)))
                self.drawx+=16
            self.drawy+=16

        self.drawy=0
        self.drawx=0








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
player.aux=0
mapa= map()
mapa.walls(0)

print mapa.wallList

def main():

    conut=0
    screenSize = (320, 480)
    window = pygame.display.set_mode( screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE )








    while 1:


        for event in pygame.event.get():
            if event.type == QUIT:
                return



        CheckInputs()
        if  player.canMove(mapa.wallList) :
            #print player.rect
            player.Move()
            player.Draw()
        #player.Move()
        #player.Draw()


        mapa.draw(0)





        pygame.display.flip()


        clock.tick (60)





if __name__ == '__main__': main()
