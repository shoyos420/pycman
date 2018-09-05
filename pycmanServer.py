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
    proxyList= []
    print("Started server")

    def dict_to_binary(the_dict):
        str = json.dumps(the_dict)
        binary = ' '.join(format(ord(letter), 'b') for letter in str)
        return binary

    def proxyPlayerStr(lista):
        lista2=[]
        for p in lista:
            lista2.append(str(p[0])+ " " + p[1])

        return lista2



    while True:

        flag=False
        ident, msg = socket.recv_multipart()


        proxy=(msg.decode())
        print(proxy)

        #msg =dict_to_binary(dictionary)
        #print (dictionary)
        for p in proxyPlayers:

            if p == ident:
                proxyList.find(str(ident))
                    a, b = n.split(' ', 1)
                    if a == str(ident):
                        proxyList.remove(n)
                proxyPlayers.remove(p)
                flag= True
        proxyPlayers.append(ident)



        #proxyList=proxyPlayerStr(proxyPlayers)
        #print(proxyList)



        for p in proxyPlayers:

            #dest, msg = p.split(' ', 1)
            #if ident ==dest.decode():
            #    print("true")
            #print(msg)
            socket.send_multipart([p, ident,msg])#bytes(dest, 'ascii')
            #print("envio")


            #socket.send_multipart([dest , ident, msg])


#        socket.send_json(dict)


if __name__ == '__main__':
	main()
