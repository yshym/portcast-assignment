from time import sleep

from redis_ import redis
from redis_.queue_ import TaskQueue
from redis_.task import Task


if __name__ == "__main__":
    numbers = [
        # containers
        "TGBU5600894",
        "TRHU5131609",
        # bills of lading
        "MEDUJ1656290",
        "MEDUJ1656241",
        "MEDUM5024051",
    ]

    for number in numbers:
        task_queue = TaskQueue("tasks", redis)
        task = Task("scrape-shipment", number)
        task_queue.push(task)
        print(f"Added '{task}' to the queue")
        sleep(4)
