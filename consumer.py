from datetime import timedelta

from prefect import task, Flow
from prefect.schedules import IntervalSchedule
from scrapyscript import Job, Processor

from database import get_db
from database.models import Container, BOL
from redis_ import redis
from redis_.queue_ import TaskQueue
from spiders.shipments_spider import ShipmentsSpider


class UnknownTaskError(Exception):
    pass


def run_shipments_spider(number):
    processor = Processor(settings={"LOG_LEVEL": "WARNING"})
    job = Job(ShipmentsSpider, number)
    return processor.run(job)


def bol_from_data(db, data):
    container_numbers = data.pop("container_numbers")
    bol = db.get(BOL, data["number"])
    if bol:
        return bol
    bol = BOL(**data)
    for number in container_numbers:
        data["number"] = number
        container = container_from_data(db, data)
        if container.bol_number != bol.number:
            bol.containers.append(container)
    print(f"Processed BOL({bol})")
    return bol


def container_from_data(db, data):
    container = db.get(Container, data["number"])
    if container:
        return container
    container = Container(**data)
    print(f"Processed Container({container})")
    return container


def process_data(db, data):
    data = {k: None if v == "" else v for k, v in data.items()}
    is_bol = "container_numbers" in data
    if is_bol:
        return bol_from_data(db, data)
    return container_from_data(db, data)


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
        db = next(get_db())
        obj = process_data(db, data)
        db.add(obj)
        db.commit()
        print(f"Task {task} succeeded")
    else:
        print(f"{task} failed")


if __name__ == "__main__":
    schedule = IntervalSchedule(interval=timedelta(seconds=20))
    with Flow("Task runner", schedule) as flow:
        run()
    flow.run()
