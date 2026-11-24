import time
import socket

SLAVE_TYPE = "B"

def process_job(job_id, job_type):
    job_type = job_type.strip().upper()

    if job_type not in ("A", "B"):
        return f"Job {job_id} has an invalid type."

    if job_type == SLAVE_TYPE:
        seconds = 2
    else:
        seconds = 10

    print(f"Slave B received job {job_id}, type {job_type}.")
    time.sleep(seconds)

    result = f"Job {job_id} completed by Slave B in {seconds} seconds."
    print(result)
    return result

slave_b_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("localhost", 5019)
slave_b_socket.connect(server_address)
print("Slave B connected to Master.")

identification = "SLAVE_B\n"
slave_b_socket.sendall(identification.encode())

while True:
    job = slave_b_socket.recv(1024).decode()

    if job == "":
        break

    job_parts = job.split(",")
    job_id = job_parts[0].split(":")[1].strip()
    job_type = job_parts[1].split(":")[1].strip()

    result = process_job(job_id, job_type)
    slave_b_socket.sendall((result + "\n").encode())
    print("Slave B informed Master that the job is complete.")

slave_b_socket.close()
