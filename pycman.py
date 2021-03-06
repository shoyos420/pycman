### creditos para forma de modelado del pacman :https://github.com/greyblue9/pacman-python
#_________/  Librerias utilizadas \__________________________#

## Pygame Utility ##
import pygame, sys, os, random, time
from pygame.locals import *

# Json utility (not used)
import json

# Socket management ZeroMQ
import zmq
from collections import namedtuple

#Matemathic utility
import binascii
import os
from random import randint

#Direccionamos nuestra carpeta para mejorar el orden#

SCRIPT_PATH=sys.path[0]


#Init del Sonido y pygame
pygame.mixer.init()

channel = pygame.mixer.Channel (2)

pickUp_small = pygame.mixer.Sound (os.path.join(SCRIPT_PATH,"res","sounds","pellet1.wav"))
moving_sound = pygame.mixer.Sound (os.path.join(SCRIPT_PATH,"res","sounds","pellet2.wav"))
pickUp_big = pygame.mixer.Sound (os.path.join(SCRIPT_PATH,"res","sounds","powerpellet.wav"))


clock = pygame.time.Clock()
pygame.init()

#definicion de nuestra ventana y pantalla
window = pygame.display.set_mode((1, 1))
pygame.display.set_caption("Pycman")
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
background = background.convert()






##______________/ Clase Pacman \____________________##


#primera definicion para el manejo de pacman en la ventana


## superclase character con los elementos mas basicos de un caracter

class Character (object):
    def __init__ (self):
        '''in - (self)'''

        self.rect = None
        self.speed = None
        self.velx = None
        self.vely = None
        self.id = None



    ## Determina si el jugador se puede mover
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

    ## Genera el movimiento en pro a su velocidad
    def Move (self):



        self.rect.top += self.vely
        self.rect.left += self.velx


    ## Funcion para definir un id obtenida desde la doc de ZeroMQ python
    def set_id(self):
        """Set simple random printable identity on socket"""
        self.id = u"%04x-%04x" % (randint(0, 0x10000), randint(0, 0x10000))



    #Determina una colision entre 2 jugadores
    def checkColl (self,jugador):

        rectTest = self.rect

        if self.velx > 0:
            rectTest = self.rect.move ((self.speed, 0))
        elif self.velx < 0:
            rectTest = self.rect.move ((-self.speed, 0))
        elif self.vely > 0:
            rectTest = self.rect.move ((0, self.speed))
        elif self.vely < 0:
            rectTest = self.rect.move ((0, -self.speed))



        if jugador.rect.colliderect (rectTest):
            return True

        return False

## clase pacman que hereda de la superclase character

class pacman (Character):

    def __init__ (self):
        #self.x = 160
        #self.y = 240
        self.identity=None
        self.velx = 0
        self.vely = 0

        self.speed=1





        self.animFrame=1
        self.animFrameG=1



        self.anim_pacmanL = {}
        self.anim_pacmanR = {}
        self.anim_pacmanU = {}
        self.anim_pacmanD = {}
        self.anim_pacmanS = {}


        self.anim_ghost = {}

        self.anim_Current = {}



        #generamos un array de nuestas imagenes
        for i in range(1, 9, 1):
            self.anim_pacmanL[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-l " + str(i) + ".gif")).convert()
            self.anim_pacmanR[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-r " + str(i) + ".gif")).convert()
            self.anim_pacmanU[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-u " + str(i) + ".gif")).convert()
            self.anim_pacmanD[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman-d " + str(i) + ".gif")).convert()
            self.anim_pacmanS[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","pacman.gif")).convert()

        for i in range (1, 7, 1):
            self.anim_ghost[i] = pygame.image.load(os.path.join(SCRIPT_PATH,"res","sprite","ghost " + str(i) + ".gif")).convert()


        self.rect=self.anim_pacmanL[1].get_rect ()



    def Draw (self):

        if self.identity == 0:
            if self.velx > 0:
                self.anim_Current = self.anim_pacmanR
            elif self.velx < 0:
                self.anim_Current = self.anim_pacmanL
            elif self.vely > 0:
                self.anim_Current = self.anim_pacmanD
            elif self.vely < 0:
                self.anim_Current = self.anim_pacmanU
            else :
                self.anim_Current = self.anim_pacmanR

            screen.blit (self.anim_Current[ self.animFrame ], (self.rect.left, self.rect.top ))

            if not self.velx == 0 or not self.vely == 0:
                # solo anima la boca cuando pacman se mueva
                self.animFrame += 1

            if self.animFrame == 9:
                # termina la animacion e inicia nuevamente
                self.animFrame = 1


        elif self.identity == 1 :

            self.anim_Current = self.anim_ghost


            screen.blit (self.anim_Current[ self.animFrameG ], (self.rect.left, self.rect.top ))

            if not self.velx == 0 or not self.vely == 0:
                # solo anima la boca cuando pacman se mueva
                self.animFrameG += 1

            if self.animFrameG == 6:
                # termina la animacion e inicia nuevamente
                self.animFrameG = 1

        #if not channel.get_busy ():
        #    channel.play (moving_sound)


        #screen.blit (self.anim_pacmanD[3], (self.x,self.y))


    def checkPellets(self):
        for i in mapa.pelletList:
            if self.rect.colliderect (i):
                mapa.pelletList.remove(i)
                if not channel.get_busy ():
                    channel.play (moving_sound)
        for i in mapa.pelletList2:
            if self.rect.colliderect (i):
                mapa.pelletList2.remove(i)
                if not channel.get_busy ():
                    channel.play (pickUp_big)
                global mode
                mode =1

                #print ("remove")
                #print (i)


##______________/ Clase Mapa \____________________##

#se encarga de definir las propiedades de un mapa y
#la definicion de unos vectores para su utilizacion en el juego

class map():
    def __init__ (self):
        self.drawx=0
        self.drawy=0
        self.wall= None
        self.pellet= pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","pellet.gif")).convert()
        self.powerPellet=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","pellet-power.gif")).convert()
        self.wallList=[]
        self.pelletList=[]
        self.pelletList2=[]



        self.colorPellets((250,250,0,255))





    def draw(self, lvl):

        #screen.fill((0,0,0))

        file = open(os.path.join(SCRIPT_PATH,"res","levels",str(lvl) + ".txt"), 'r')

        for line in file:
            self.drawx=0
            for caracter in line:
                if caracter == '#':
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-straight-horiz.gif")).convert()
                    self.colorWall((6, 6, 118, 255),(100, 100, 250, 255),(5, 5, 50, 255))
                    screen.blit (self.wall, (self.drawx, self.drawy ))

                elif caracter == '$':
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-straight-vert.gif")).convert()
                    self.colorWall((6, 6, 118, 255),(100, 100, 250, 255),(5, 5, 50, 255))
                    screen.blit (self.wall, (self.drawx, self.drawy ))

                elif caracter == 'd':
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","ghost-door.gif")).convert()
                    self.colorWall((6, 6, 118, 255),(100, 100, 250, 255),(5, 5, 50, 255))
                    screen.blit (self.wall, (self.drawx, self.drawy ))

                elif caracter == '1' or caracter == '2' or caracter =='3' or caracter == '4' :
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-edge" + caracter + ".gif")).convert()
                    self.colorWall((6, 6, 118, 255),(100, 100, 250, 255),(5, 5, 50, 255))
                    screen.blit (self.wall, (self.drawx, self.drawy ))
                elif caracter == 'r' or caracter == 'b' or caracter =='t' or caracter == 'l' :
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-end-" + caracter + ".gif")).convert()
                    self.colorWall((6, 6, 118, 255),(100, 100, 250, 255),(5, 5, 50, 255))
                    screen.blit (self.wall, (self.drawx, self.drawy ))

                elif caracter == 'y' or caracter == 'v' or caracter =='>' or caracter == '<':
                    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","wall-t-"+ caracter+".gif")).convert()
                    self.colorWall((6, 6, 118, 255),(100, 100, 250, 255),(5, 5, 50, 255))
                    screen.blit (self.wall, (self.drawx, self.drawy ))

                #if caracter == 'p':
                #    self.wall=pygame.image.load(os.path.join(SCRIPT_PATH,"res","tiles","pellet.gif")).convert()
                #    screen.blit (self.wall, (self.drawx, self.drawy ))

                self.drawx+=16
            self.drawy+=16

        self.drawy=0
        self.drawx=0

    def drawPellets(self, lvl):

        #screen.fill((0,0,0))

        file = open(os.path.join(SCRIPT_PATH,"res","levels",str(lvl) + ".txt"), 'r')

        for p in self.pelletList:
            screen.blit (self.pellet, (p.left, p.top ))

        for p in self.pelletList2:

            screen.blit (self.powerPellet, (p.left, p.top ))


    def colorWall(self,color,light,shadow):
        for y in range(0, 16, 1):
            for x in range(0, 16, 1):

                if self.wall.get_at((x, y))==(255, 206, 255, 255):
                    self.wall.set_at( (x, y), light )

                if self.wall.get_at((x, y))==(132, 0, 132, 255):
                    self.wall.set_at( (x, y), color )

                if self.wall.get_at((x, y))==(255, 0, 255, 255):
                    self.wall.set_at( (x, y), color )

    def colorPellets(self,color):
        for y in range(0, 16, 1):
            for x in range(0, 16, 1):

                if self.pellet.get_at((x, y))== (128, 0, 128, 255):
                    self.pellet.set_at( (x, y), color )
                if self.powerPellet.get_at((x, y))== (128, 0, 128, 255):
                    self.powerPellet.set_at( (x, y), color )








    def Obstacles(self,lvl):

        file = open(os.path.join(SCRIPT_PATH,"res","levels",str(lvl) + ".txt"), 'r')

        for line in file:
            self.drawx=0
            for caracter in line:
                if caracter == '#':
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (12, 12)))
                if caracter == '$':
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (12, 12)))
                if caracter == '1' or caracter == '2' or caracter =='3' or caracter == '4' :
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (12, 12)))
                if caracter == 'r' or caracter == 'b' or caracter =='t' or caracter == 'l':
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (12, 12)))
                if caracter == '1' or caracter == '2' or caracter =='3' or caracter == '4' :
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (12, 12)))
                if caracter == 'r' or caracter == 'b' or caracter =='t' or caracter == 'l' :
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (12, 12)))
                if caracter == 'y' or caracter == 'v' or caracter =='>' or caracter == '<':
                    self.wallList.append(pygame.Rect((self.drawx, self.drawy), (12, 12)))
                if caracter == 'p':
                    self.pelletList.append(pygame.Rect((self.drawx, self.drawy), (8, 8)))
                if caracter == 'P':
                    self.pelletList2.append(pygame.Rect((self.drawx, self.drawy), (8, 8)))
                self.drawx+=16
            self.drawy+=16

        self.drawy=0
        self.drawx=0









#______________/ entradas y controles\____________________________

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


#controles secundarios (WASD) no utilizados
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




## envio asincrono de datos , manda las propiedades del jugador de esta ventana
def enviar():

    socket.send_multipart([bin(player.rect.left) , bin(player.rect.top) ,bin(player.velx) ,bin(player.velx),bin(player.identity)])

## obtencion asincrona de datos , recibe las propiedades de los demas jugadores de esta ventana
def recibir():
    #lista= playerList


    id, x , y, velx ,vely, identity = socket.recv_multipart()
    if not id in idList:
        idList.append(id)

    proxyPlayer= pacman()
    proxyPlayer.id=id.decode('ascii')
    #proxyPlayer.identity=randint(0, 1)
    proxyPlayer.rect.left=int(x.decode(),2)
    proxyPlayer.rect.top=int(y.decode(),2)
    proxyPlayer.velx=int(velx.decode(),2)
    proxyPlayer.vely=int(vely.decode(),2)
    proxyPlayer.identity=int(identity.decode(),2)


    for p in playerList:
        if p.id == proxyPlayer.id:
            playerList.remove(p)

    playerList.append(proxyPlayer)


##  define que identidad tendras antes de iniciar (pacman o fantasma)
## y tu posicion en el mapa
def inicializador():
    player.identity=randint(0, 1)

    if player.identity == 0:

        player.rect.top=336
        player.rect.left=136
    else :

        player.rect.top=224
        player.rect.left=136




#______________/ game init \____________________________




player = pacman()
inicializador()


playerList = []

idList=[]

mapa= map()
mapa.Obstacles(0)


 ##_______________________________________/ SOCKET CONETTION INIT \____________________________________
if len(sys.argv) != 2:
    print("Must be called with an identity")
    exit()
context = zmq.Context()
socket = context.socket(zmq.DEALER)
player.id = sys.argv[1].encode('ascii')
socket.identity = player.id
socket.connect("tcp://localhost:4444")
print("Started client with id {}".format(player.id))
poller = zmq.Poller()
poller.register(sys.stdin, zmq.POLLIN)
poller.register(socket, zmq.POLLIN)



def main():


    screenSize = (304, 480)
    window = pygame.display.set_mode( screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE )

    # dibujamos el mapa y generamos un background para no realizar el dibujado
    # Multiples ocaciones

    mapa.draw(0)
    background = screen.copy()
    enviar()
    recibir()

    #loop de juego pygame
    while 1:
        enviar()
        for p in playerList:
            recibir()





        screen.blit(background,(0,0))


        for event in pygame.event.get():
            if event.type == QUIT:
                return


        #revisa movimiento
        CheckInputs()

        #si se puede mover:
        if  player.canMove() :
            #el jugador se mueve
            player.Move()
            #si es un pacman come pellets
            if player.identity == 0:
                player.checkPellets()

        for p in playerList :
            #si se puede mover:
            if  p.canMove() :
                #el jugador se mueve
                p.Move()
                if p.identity == 0:
                    #si es un pacman come pellets
                    p.checkPellets()
            # si se encuentran 2 caracteres el pacman se vuelve fantasma
            if p.checkColl(player):
                if p.identity == 1:
                    player.identity = 1

        ## dibujamos los pellets actuales
        mapa.drawPellets(0)
        ## dibujamos al jugador de esta ventana
        player.Draw()
        ## dibujamos a los demas jugadores
        for p in playerList :
            p.Draw()

        # rutinario de pygame para visualizacion
        pygame.display.flip()
        clock.tick (60)






if __name__ == '__main__': main()
