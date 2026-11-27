import socket
import time
import random


client_id = random.randint(10,99)
NUMBER_OF_JOBS = 6
jobs = []
for i in range(NUMBER_OF_JOBS):
    job_type = "B" if i == 1 else "A"
    job = {"id": i + 1, "type": job_type}
    jobs.append(job)
    print(f"Client created job {i + 1}-{client_id} of type {job_type}")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5019)
client_socket.connect(server_address)
print("Client is connecting...")

identification = "CLIENT\n"
client_socket.send(identification.encode())
#make sure the messages do not get sent in one package
time.sleep(0.1)


for job in jobs:
    job_id = job["id"]
    job_type = job["type"]
    job = f"ID: {job_id}-{client_id}, Type: {job_type} \n"
    client_socket.send(job.encode())
    print(f"Client has submitted job {job_id}-{client_id} to Master")

completed = 0
while completed < NUMBER_OF_JOBS:
    result = client_socket.recv(1024).decode()
    if not result:
        break
    res = result.split("\n")
    for r in res:
        if r.strip() != "":
            completed += 1
            print(f"Client {client_id} informed user: {r}.")

client_socket.close()