#!/usr/bin/env python3
"""Script Python per la realizzazione di un Server multithread
per connessioni CHAT asincrone.
Corso di Programmazione di Reti - Università di Bologna"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

""" La funzione che segue accetta le connessioni  dei client in entrata."""
def accept_entrance_connections ():
    while True:
     #   try: 
            client, client_address = SERVER.accept()
            print("%s:%s si è collegato." % client_address)
            #al client che si connette per la prima volta fornisce alcune indicazioni di utilizzo
            client.send(bytes("Salve! Digita il tuo Nome seguito dal tasto Invio!", "utf8"))
            # ci serviamo di un dizionario per registrare i client
            addresses[client] = client_address
            #diamo inizio all'attività del Thread - uno per ciascun client
            Thread(target=handle_client, args=(client,)).start()
          
    #    except:
            
            

"""La funzione seguente gestisce la connessione di un singolo client."""
def handle_client(client):  # Prende il socket del client come argomento della funzione.
    
    try:
        
        nome = client.recv(BUFSIZ).decode("utf8")
        if not nome:
            remove(client)
        #da il benvenuto al client e gli indica come fare per uscire dalla chat quando ha terminato
        benvenuto = 'Benvenuto %s! Se vuoi lasciare la Chat, scrivi {quit} per uscire.' % nome
        client.send(bytes(benvenuto, "utf8"))
        msg = "%s si è unito all chat!" % nome        
        #messaggio in broadcast con cui vengono avvisati tutti i client connessi che l'utente x è entrato
        broadcast(bytes(msg, "utf8"))
        #aggiorna il dizionario clients creato all'inizio
        clients[client] = nome
    except():
        remove(client)
    
    #si mette in ascolto del thread del singolo client e ne gestisce l'invio dei messaggi o l'uscita dalla Chat
    while True:
        try:
            msg = client.recv(BUFSIZ)
        
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, nome+": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                remove(client, nome)
                break
        except():
            broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8"))

""" La funzione, che segue, invia un messaggio in broadcast a tutti i client."""
def broadcast(msg, prefisso=""):  # il prefisso è usato per l'identificazione del nome.
    for utente in clients:
        utente.send(bytes(prefisso, "utf8")+msg)
" Rimuove il client, se viene specificato il nome ne annuncia l'abbandono"
def remove(client, nome=''):
    client.close()
    del clients[client]
    if nome:
        broadcast(bytes("%s ha abbandonato la Chat." % nome, "utf8"))
    
    
    
    
clients = {}
addresses = {}

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accept_entrance_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
