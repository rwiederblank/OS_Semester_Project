import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5013))
server_socket.listen()
print("Server is listening...")
conn, address = server_socket.accept()
print("Client connected!!!")

while True:
    job = conn.recv(1024).decode()
    if not job:
        break
    print(f"Received Job: {job}")
