from random import randrange
from time import sleep

from redis_ import redis
from redis_.queue_ import TaskQueue
from redis_.task import Task


if __name__ == "__main__":
    while True:
        task_queue = TaskQueue("tasks", redis)
        x1, x2 = randrange(1, 11), randrange(1, 11)
        task_queue.push(Task("sum", x1, x2))
        sleep(3)
