import os
import time

import gitlab


gl = gitlab.Gitlab(
    "https://gitlab.com",
    private_token=os.getenv("GITLAB_TOKEN"),
)

project = gl.projects.get(41907652)
pipeline = project.pipelines.get(1029650556)
jobs = pipeline.jobs.list(get_all=True)
for job in jobs:
    print(job.id, job.name, job.status)
job = project.jobs.get("5247406815")
print(job.status)
trace_len = 0
while True:
    current_trace = job.trace().decode("utf-8")
    if len(current_trace) > trace_len:
        print(current_trace[trace_len:])
        trace_len = len(current_trace)
    time.sleep(1)
    print("checking..")
