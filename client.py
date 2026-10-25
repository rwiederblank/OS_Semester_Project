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
