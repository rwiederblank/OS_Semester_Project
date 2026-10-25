import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5011))
server_socket.listen()
print("Server is listening...")
server_socket.accept()
print("Client connected!!!")
