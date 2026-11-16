import time

SLAVE_TYPE = "A"

def process_job(job_id, job_type):
    job_type = job_type.strip().upper()

    if job_type not in ("A", "B"):
        return f"Job {job_id} has an invalid type."

    if job_type == SLAVE_TYPE:
        seconds = 2
    else:
        seconds = 10

    print(f"Slave A received job {job_id}, type {job_type}.")
    time.sleep(seconds)

    result = f"Job {job_id} completed by Slave A in {seconds} seconds."
    print(result)
    return result