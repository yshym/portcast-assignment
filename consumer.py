from datetime import timedelta

from scrapyscript import Job, Processor
from sqlmodel import Session
from prefect import task, Flow
from prefect.schedules import IntervalSchedule

from db import engine
from db.models import Container, BOL
from redis_ import redis
from redis_.queue_ import TaskQueue
from spiders.shipments_spider import ShipmentsSpider


class UnknownTaskError(Exception):
    pass


def run_shipments_spider(number):
    processor = Processor(settings={"LOG_LEVEL": "WARNING"})
    job = Job(ShipmentsSpider, number)
    return processor.run(job)


def bol_from_data(session, data):
    container_numbers = data.pop("container_numbers")
    bol = session.get(BOL, data["number"])
    if bol:
        return bol
    bol = BOL(**data)
    for number in container_numbers:
        container_data = run_shipments_spider(number)
        if container_data:
            container = container_from_data(session, container_data[0])
            if container.bol_number != bol.number:
                bol.containers.append(container)
    print(f"Processed BOL({bol})")
    return bol


def container_from_data(session, data):
    container = session.get(Container, data["number"])
    if container:
        return container
    container = Container(**data)
    print(f"Processed Container({container})")
    return container


def process_data(session, data):
    data = {k: None if v == "" else v for k, v in data.items()}
    is_bol = "container_numbers" in data
    if is_bol:
        return bol_from_data(session, data)
    return container_from_data(session, data)


@task
def run():
    task_queue = TaskQueue("tasks", redis)
    task = task_queue.pop()
    if not task:
        return
    print(f"Executing {task}...")
    if task.name != "scrape-shipment":
        raise UnknownTaskError(f"task '{task.name}' is not known")
    data = run_shipments_spider(task.args[0])
    if data:
        data = data[0]
        with Session(engine) as session:
            obj = process_data(session, data)
            session.add(obj)
            session.commit()
            print(f"Task {task} succeeded")
    else:
        print(f"{task} failed")


if __name__ == "__main__":
    schedule = IntervalSchedule(interval=timedelta(minutes=5))
    with Flow("Task runner", schedule) as flow:
        run()
    flow.run()
