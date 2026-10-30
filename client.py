import socket

NUMBER_OF_JOBS = 4
jobs = []
for i in range(NUMBER_OF_JOBS):
    if i % 2 == 0:
        job = {"id":i+1, "type":"A"}
        jobs.append(job)
        print(f"Client created job {i+1} of type A")
    else:
        job = {"id": i + 1, "type": "B"}
        jobs.append(job)
        print(f"Client created job {i+1} of type B")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5016)
client_socket.connect(server_address)
print("Client is connecting...")

for job in jobs:
    job_id = job["id"]
    job_type = job["type"]
    job = f"ID: {job_id}, Type: {job_type} \n"
    client_socket.send(job.encode())
    print(f"Client has submitted job {job_id} to Master")
