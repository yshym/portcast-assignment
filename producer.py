from collections import deque
from datetime import timedelta

import prefect
from prefect import Flow
from prefect.schedules import IntervalSchedule
from redis_ import redis
from redis_.queue_ import TaskQueue
from redis_.task import Task


numbers = deque([
    # containers
    "TGBU5600894",
    "TRHU5131609",
    # bills of lading
    "MEDUJ1656290",
    "MEDUJ1656241",
    "MEDUM5024051",
])


@prefect.task
def run():
    global numbers
    if not numbers:
        print("Numbers list is empty")
        return
    number = numbers.popleft()
    task_queue = TaskQueue("tasks", redis)
    task = Task("scrape-shipment", number)
    task_queue.push(task)
    print(f"Added '{task}' to the queue")


if __name__ == "__main__":
    schedule = IntervalSchedule(interval=timedelta(minutes=4))
    with Flow("Producer", schedule) as flow:
        run()
    flow.run()
