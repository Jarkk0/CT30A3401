import socket
import threading

# define host IP and port
HOST = '127.0.0.1'
PORT = 5555

# create socket object and bind to host and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# list to hold all client connections
clients = []

# function to handle each client connection
def handle_client(conn, addr):
    # send welcome message to client
    conn.send("Welcome to the chatroom!".encode())

    # prompt client for nickname
    conn.send("Please enter your nickname: ".encode())
    nickname = conn.recv(1024).decode()

    # add client to list of clients
    clients.append((conn, nickname))

    # loop to receive messages from client
    while True:
        try:
            # receive message from client
            message = conn.recv(1024).decode()

            # check if message is a private message
            if message.startswith('/p '):
                # get recipient and message content
                recipient, message = message.split()[1], ' '.join(message.split()[2:])
                # send private message to recipient
                for client in clients:
                    if client[1] == recipient:
                        client[0].send(f'(Private Message) {nickname}: {message}'.encode())
                        break
            else:
                # send message to all clients
                for client in clients:
                    if client[0] != conn:
                        client[0].send(f'{nickname}: {message}'.encode())

        except:
            # remove client from list of clients
            clients.remove((conn, nickname))
            conn.close()
            break

# function to start the server and listen for client connections
def start_server():
    # start listening for connections
    server.listen()

    while True:
        # accept client connection
        conn, addr = server.accept()

        # create thread to handle client connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# start the server
print("Starting server...")
start_server()
