import threading
import socket 

host = '172.16.8.238'
port = 50001

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
server.bind(("0.0.0.0",port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]    
            broadcast(f'{nickname} left the chat '.encode('ascii'))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        
        nicknames.append(nickname)
        clients.append(client)
        
        try:
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii').strip()
    
            if not nickname:
                print(f"Client at {address} did not send a nickname. Disconnecting.")
                client.close()
                continue
        except ConnectionResetError:
            print(f"Client at {address} disconnected before sending nickname.")
            client.close()
            continue
        
        try:
            client.send('Connected to the server'.encode('ascii'))
        except ConnectionResetError:
            print(f"Could not send welcome message to {nickname}")
            continue

        thread = threading.Thread(target = handle, args=(client,))
        thread.start()

print("Server is listening ...... ")

recieve()





