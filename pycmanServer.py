
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
aux=0


while True:
    flag=False

    #  espera al siguiente mensaje del cliente
    message = socket.recv_json()
    ##print("Received request: %s" % message)

    #dictionary={'id': message[0] , 'rect': message[1] , 'velx': message[2] , 'vely': message[3] ,'pellets': message[4]}

    dictionary={'id': message[0] , 'posy': message[1] , 'posx': message[2] ,'velx' : message[3] ,'vely' : message[4]} ## , 'pellets': message[5]}






    for e in proxyPlayers:
        if e['id'] == dictionary['id']:
            proxyPlayers.remove(e)
            flag= True



    if  not flag :
        proxyPlayers.append(dictionary)
        print("no estaba")
    else :
        proxyPlayers.append(dictionary)
        if aux==0:
            print(proxyPlayers[0])
            aux+=1

    print(len(proxyPlayers))

    #  Do some 'work'
    #time.sleep(1)

    #  devuelve el mensaje al cliente

    socket.send_json(proxyPlayers)
