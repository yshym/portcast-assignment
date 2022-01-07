import json
from typing import Callable


class Task:
    def __init__(self, name: str, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def __call__(self, function: Callable):
        return function(*self.args, **self.kwargs)

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def __repr__(self):
        return self.__str__()

    def dumps(self) -> str:
        return json.dumps(self, cls=TaskJSONEncoder)

    @classmethod
    def loads(cls, s: str) -> "Task":
        return json.loads(s, cls=TaskJSONDecoder)


class TaskJSONEncoder(json.JSONEncoder):
    def default(self, task: Task):
        return {"name": task.name, "args": task.args, "kwargs": task.kwargs}


class TaskJSONDecoder(json.JSONDecoder):
    def decode(self, s):
        d = json.loads(s)
        return Task(d["name"], *d["args"], **d["kwargs"])
