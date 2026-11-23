import socket
import threading
from queue import Queue

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5019))
server_socket.listen()
print("Server is listening...")

job_queue_a = Queue()
job_queue_b = Queue()
total_remaining_a = 0
total_remaining_b = 0

lock = threading.Lock()


def handle_client(client_socket):
    global total_remaining_a, total_remaining_b
    while True:
        job = client_socket.recv(1024).decode()
        if not job:
            break
        job_list = job.split("\n")
        for j in job_list:
            if j.strip() == "":
                continue
            print(f"Received Job: {j}")
            job = j.split(",")
            split_zero = job[0].split(":")
            job_id = split_zero[1].strip()

            split_one = job[1].split(":")
            job_type = split_one[1].strip()

            cost_slave_a = 0
            cost_slave_b = 0

            if job_type == "A":
                cost_slave_a = 2
                cost_slave_b = 10
            else:
                cost_slave_b = 2
                cost_slave_a = 10

            with lock:
                projected_a = total_remaining_a + cost_slave_a
                projected_b = total_remaining_b + cost_slave_b
                if projected_a <= projected_b:
                    total_remaining_a += cost_slave_a
                    print("Master assigned job to Slave A.")
                    job_queue_a.put((job_id, job_type, cost_slave_a, client_socket))
                else:
                    total_remaining_b += cost_slave_b
                    print("Master assigned job to Slave B.")
                    job_queue_b.put((job_id, job_type, cost_slave_b, client_socket))


def slave_handler(slave_socket, slave_name, slave_type):
    global total_remaining_a, total_remaining_b
    while True:
        job_id, job_type, job_cost, client_socket = slave_type.get()
        try:
            job_message = f'ID:{job_id}, Type:{job_type}\n'
            slave_socket.sendall(job_message.encode())
            result = slave_socket.recv(1024).decode().strip()
            print(f"Result: {result}")
            if not result:
                print(f"{slave_name} disconnected.")
                break

            print(f"Master received completion from {slave_name}.")

            try:
                client_socket.sendall((result + "\n").encode())
            except OSError as error:
                print(f"Could not communicate with {client_socket}: {error}")

            print("Master informed client that job was completed successfully.")

        except OSError as error:
            print(f"Could not communicate with {slave_name}: {error}")
            break
        finally:
            with lock:
                if slave_name == "SLAVE_A":
                    total_remaining_a -= job_cost
                else:
                    total_remaining_b -= job_cost
                slave_type.task_done()


def main():
    while True:
        client_socket, client_address = server_socket.accept()
        identification = client_socket.recv(1024).decode().strip()
        if identification == "CLIENT":
            print("Client connected!")
            threading.Thread(target=handle_client, args=(client_socket,)).start()
        elif identification == "SLAVE_A":
            print("Slave A Connected!")
            threading.Thread(target=slave_handler, args=(client_socket, identification, job_queue_a)).start()
        elif identification == "SLAVE_B":
            print("Slave B Connected!")
            threading.Thread(target=slave_handler, args=(client_socket, identification, job_queue_b)).start()

main()