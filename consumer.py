from operator import add
from time import sleep

from sqlmodel import Session

from db import engine
from db.models import SumResult
from producer import Task
from redis_ import redis
from redis_.queue_ import TaskQueue


def execute_task(task: Task):
    if task.name == "sum":
        return task(add)


if __name__ == "__main__":
    while True:
        task_queue = TaskQueue("tasks", redis)
        task = task_queue.pop()
        res = execute_task(task)
        with Session(engine) as session:
            sum_result = SumResult(result=res)
            session.add(sum_result)
            session.commit()
            print(sum_result.result)
        sleep(5)
