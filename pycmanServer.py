
#
#   cliente de pycman
#   utiliza un gran diccionario de jugadores
#   comprueba si ese jugador existe y devuelve el diccionario actualizado
#   se recomienda hacer una intercepcion de listas de pellets en el lado del cliente
#

import time
import zmq



context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")
proxyPlayers=[]

while True:
    #  espera al siguiente mensaje del cliente
    message = socket.recv_json()
    ##print("Received request: %s" % message)

    #dictionary={'id': message[0] , 'rect': message[1] , 'velx': message[2] , 'vely': message[3] ,'pellets': message[4]}

    dictionary={'id': message[0] , 'posx': message[1] , 'posy': message[2] ,  'pellets': message[3]}

    if  not proxyPlayers.count(dictionary) :
        proxyPlayers.append(dictionary)
        print("no estaba")



    #  Do some 'work'
    time.sleep(1)

    #  devuelve el mensaje al cliente

    socket.send_json(proxyPlayers)
