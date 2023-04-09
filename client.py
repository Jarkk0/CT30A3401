import socket
import threading

# define host IP and port
HOST = '127.0.0.1'
PORT = 5555

# create socket object and connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# function to receive messages from server
def receive_messages():
    while True:
        try:
            # receive message from server
            message = client.recv(1024).decode()

            # print message to console
            print(message)
        except:
            # if an error occurs, close the connection
            client.close()
            break

# function to send messages to server
def send_message():
    while True:
        # get message from user input
        message = input()

        # send message to server
        client.send(message.encode())

# prompt user for nickname
nickname = input("Please enter your nickname: ")

# send nickname to server
client.send(nickname.encode())

# create threads for sending and receiving messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()
