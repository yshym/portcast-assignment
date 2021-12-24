from operator import add
from time import sleep

from producer import Task
from redis_.client import redis
from redis_.queue_ import TaskQueue


def execute_task(task: Task):
    if task.name == "sum":
        return task(add)


if __name__ == "__main__":
    while True:
        task_queue = TaskQueue("tasks", redis)
        task = task_queue.pop()
        res = execute_task(task)
        print(res)
        sleep(5)
