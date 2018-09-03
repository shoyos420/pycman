
#libreria pygame
import pygame, sys, os, random, time
from pygame.locals import *

import zmq

import binascii
import os
from random import randint

#direccionamos nuestra carpeta para mejorar el orden

SCRIPT_PATH=sys.path[0]

pygame.mixer.init()

channel = pygame.mixer.Channel (2)

pickUp_small = pygame.mixer.Sound (os.path.join(SCRIPT_PATH,"res","sounds","pellet1.wav"))
moving_sound = pygame.mixer.Sound (os.path.join(SCRIPT_PATH,"res","sounds","pellet2.wav"))



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

        self.rect = None
        self.speed = None
        self.velx = None
        self.vely = None
        self.id = None

        #self.x= None
        #sef.y= None

    def canMove (self):

        rectTest = self.rect

        if self.velx > 0:
            rectTest = self.rect.move ((self.speed, 0))
        elif self.velx < 0:
            rectTest = self.rect.move ((-self.speed, 0))
        elif self.vely > 0:
            rectTest = self.rect.move ((0, self.speed))
        elif self.vely < 0:
            rectTest = self.rect.move ((0, -self.speed))


        for wall in mapa.wallList:
            if wall.colliderect (rectTest):
                return False

        return True

    def Move (self):



        self.rect.top += self.vely
        self.rect.left += self.velx

    def set_id(self):
        """Set simple random printable identity on socket"""
        self.id = u"%04x-%04x" % (randint(0, 0x10000), randint(0, 0x10000))


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
        self.rect.top=340
        self.rect.left=160


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

        #if not channel.get_busy ():
        #    channel.play (moving_sound)
        screen.blit (self.anim_pacmanCurrent[ self.animFrame ], (self.rect.left, self.rect.top ))

        #screen.blit (self.anim_pacmanD[3], (self.x,self.y))

        if not self.velx == 0 or not self.vely == 0:
            # solo anima la boca cuando pacman se mueva
            self.animFrame += 1

        if self.animFrame == 9:
            # termina la animacion e inicia nuevamente
            self.animFrame = 1

    def checkPellets(self):
        for i in mapa.pelletList:
            if self.rect.colliderect (i):
                mapa.pelletList.remove(i)
                if not channel.get_busy ():
                    channel.play (moving_sound)
                print "remove"
                print i




class map():
    def __init__ (self):
        self.drawx=0
        self.drawy=0
        self.wall= None
        self.wallList=[]
        self.pelletList=[]









    def draw(self, lvl):

        #screen.fill((0,0,0))

        file = open(os.path.join(SCRIPT_PATH,"res","levels",str(lvl) + ".txt"), 'r')

        for line in file:
            self.drawx=0
            for caracter in line:
                if caracter == '#':
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-straight-horiz.gif")).convert()
                    screen.blit (self.wall, (self.drawx, self.drawy ))

                if caracter == '$':
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-straight-vert.gif")).convert()
                    screen.blit (self.wall, (self.drawx, self.drawy ))

                if caracter == '1' or caracter == '2' or caracter =='3' or caracter == '4' :
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-edge" + caracter + ".gif")).convert()
                    screen.blit (self.wall, (self.drawx, self.drawy ))
                if caracter == 'r' or caracter == 'b' or caracter =='t' or caracter == 'l' :
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-end-" + caracter + ".gif")).convert()
                    screen.blit (self.wall, (self.drawx, self.drawy ))

                if caracter == 'y' or caracter == 'v' or caracter =='>' or caracter == '<':
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-t-"+ caracter+".gif")).convert()
                    screen.blit (self.wall, (self.drawx, self.drawy ))
                #if caracter == 'p':
                #    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","pellet.gif")).convert()
                #    screen.blit (self.wall, (self.drawx, self.drawy ))

                self.drawx+=16
            self.drawy+=16

        self.drawy=0
        self.drawx=0

        for p in self.pelletList:
            self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","pellet.gif")).convert()
            screen.blit (self.wall, (p.left, p.top ))






    def Obstacles(self,lvl):

        file = open(os.path.join(SCRIPT_PATH,"res","levels",str(lvl) + ".txt"), 'r')

        for line in file:
            self.drawx=0
            for caracter in line:
                if caracter == '#':
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (14, 14)))
                if caracter == '$':
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (14, 14)))
                if caracter == '1' or caracter == '2' or caracter =='3' or caracter == '4' :
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (12, 12)))
                if caracter == 'r' or caracter == 'b' or caracter =='t' or caracter == 'l':
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (12, 12)))
                if caracter == 'p':
                    self.pelletList.append(pygame.Rect((self.drawx, self.drawy), (8, 8)))
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

def CheckInputs2():


    if pygame.key.get_pressed()[ pygame.K_d ] :

        player2.velx = player2.speed
        player2.vely = 0



    elif pygame.key.get_pressed()[ pygame.K_a] :

        player2.velx = -player2.speed
        player2.vely = 0

    elif pygame.key.get_pressed()[ pygame.K_s ] :
        player2.velx = 0
        player2.vely = player2.speed


    elif pygame.key.get_pressed()[ pygame.K_w ] :

        player2.velx = 0
        player2.vely = -player.speed



    if pygame.key.get_pressed()[ pygame.K_ESCAPE ]:
        sys.exit(0)


def conection():
    context = zmq.Context()


    #  Socket to talk to server
    print("Connecting to pycman server...")
    socket = context.socket(zmq.REQ)



    socket.connect("tcp://localhost:5556")




    #  Do 10 requests, waiting each time for a response

    print("Sending request")
    actualStats = [player.id , player.rect.top, player.rect.left , mapa.pelletList]
    socket.send_json(actualStats)

        #  Get the reply.
    message = socket.recv_json()
    print(message[0]['id'])
        #print("Received reply %s [ %s ]" % (request, message))


#______________/ game init \____________________________

player = pacman()
player.set_id()
print(player.id)
player2 = pacman()

mapa= map()
mapa.Obstacles(0)


##print len(mapa.wallList)

def main():


    screenSize = (304, 480)
    window = pygame.display.set_mode( screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE )



    conection()




    while 1:


        for event in pygame.event.get():
            if event.type == QUIT:
                return


        screen.fill((0,0,0))
        CheckInputs()
        if  player.canMove() :
            #print player.rect
            player.Move()
            player.checkPellets()
        player.Draw()
        #player.Move()
        #player.Draw()

        CheckInputs2()
        if  player2.canMove() :
            #print player2.rect
            player2.Move()
            player2.checkPellets()
        player2.Draw()

        mapa.draw(0)





        pygame.display.flip()


        clock.tick (60)





if __name__ == '__main__': main()
