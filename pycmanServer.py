#   cliente de pycman
#   utiliza un gran diccionario de jugadores
#   comprueba si ese jugador existe y devuelve el diccionario actualizado
#   se recomienda hacer una intercepcion de listas de pellets en el lado del cliente

import zmq
import sys
from collections import namedtuple
import json

def main():
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind("tcp://*:4444")
    proxyPlayers = []
    identList= []
    print("Started server")





    while True:

        #flag=False

        ident, x, y , velx , vely , identity= socket.recv_multipart()
        #proxy=int(msg.decode(),2)
        #print(proxy)

        if not ident in identList:
            identList.append(ident)

        for p in identList:


            if p != ident:

                socket.send_multipart([p, ident,x , y , velx, vely, identity ])

            #socket.send_multipart([dest , ident, msg])


#        socket.send_json(dict)


if __name__ == '__main__':
	main()
