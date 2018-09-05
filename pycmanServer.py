#   cliente de pycman
#   utiliza un gran diccionario de jugadores
#   comprueba si ese jugador existe y devuelve el diccionario actualizado
#   se recomienda hacer una intercepcion de listas de pellets en el lado del cliente

import zmq
import sys
from collections import namedtuple

def main():
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind("tcp://*:4444")
    proxyPlayers = []
    print("Started server")

    while True:

        flag=False
        ident, message = socket.recv_multipart()

        #dictionary={'id': message[0] , 'posy': message[1] , 'posx': message[2] ,'velx' : message[3] ,'vely' : message[4]} ## , 'pellets': message[5]}

        #for e in proxyPlayers:
        #    if e['id'] == dictionary['id']:
        #        proxyPlayers.remove(e)
        #        flag= True

        #proxyPlayers.append(dictionary)



        print("Message received from {}".format(message[1]))

            #socket.send_multipart([dest , ident, msg])
        socket.send_multipart([ident, message])


if __name__ == '__main__':
	main()
