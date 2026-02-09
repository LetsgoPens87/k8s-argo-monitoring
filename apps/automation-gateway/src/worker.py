import redis
import json
import time
from datetime import datetime

# Connect to Redis
r = redis.Redis(host='redis', port=6379)

def process_job(job):
    job_id = job['id']
    jobs[job_id]['status'] = 'RUNNING'
    jobs[job_id]['started_at'] = datetime.utcnow().isoformat()

    try:
        # Simulate doing work
        time.sleep(random.uniform(1, 3))
        if random.random() < 0.1:
            raise Exception("Simulated failure")
        # Mark success
        jobs[job_id]['status'] = 'SUCCESS'
    except Exception as e:
        jobs[job_id]['status'] = 'FAILED'
        jobs[job_id]['error'] = str(e)
    finally:
        jobs[job_id]['finished_at'] = datetime.utcnow().isoformat()

        # Record duration
        start = datetime.fromisoformat(jobs[job_id]['started_at'])
        end = datetime.fromisoformat(jobs[job_id]['finished_at'])
        duration = (end - start).total_seconds()

        # Update metrics if needed
        # e.g., automation_job_duration_seconds.labels(action=job['action']).observe(duration)

# Worker loop
while True:
    # Wait for a job
    job_json = r.brpop("job_queue", timeout=0)
    if job_json:
        _, job_str = job_json
        job = json.loads(job_str)
        process_job(job)