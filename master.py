import socket
import threading
from queue import Queue

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5016))
server_socket.listen()
print("Server is listening...")

job_queue = Queue()

def handle_client(client_socket):
    while True:
        job = client_socket.recv(1024).decode()
        if not job:
            break
        print(f"Received Job: {job}")
        job = job.split(",")
        split_zero = job[0].split(":")
        job_id = split_zero[1].strip()

        split_one = job[1].split(":")
        job_type = split_one[1].strip()

        job_queue.put((job_id, job_type))

    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    print("Client connected!")
    threading.Thread(target=handle_client, args=(client_socket,)).start()