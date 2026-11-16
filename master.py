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

def slave_handler(slave_socket, slave_name):
    while True:
        job_id, job_type = job_queue.get()
        try:
            job_message = f'ID:{job_id}, Type:{job_type}\n'
            slave_socket.sendall(job_message.encode())
            result = slave_socket.recv(1024).decode().strip()
            print(f"Result: {result}")
            if not result:
                print(f"{slave_name} disconnected.")
                break
        except OSError as error:
            print(f"Could not communicate with {slave_name}: {error}")
            break
        finally:
            job_queue.task_done()


def main():
    while True:
        client_socket, client_address = server_socket.accept()
        identification = client_socket.recv(1024).decode().strip()
        if identification == "CLIENT":
            print("Client connected!")
            threading.Thread(target=handle_client, args=(client_socket,)).start()
        elif identification == "SLAVE_A":
            print("Slave A Connected!")
            threading.Thread(target=slave_handler, args=(client_socket, identification)).start()
        elif identification == "SLAVE_B":
            print("Slave B Connected!")
            threading.Thread(target=slave_handler, args=(client_socket, identification)).start()


main()



