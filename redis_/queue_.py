from redis import Redis

from .task import Task


class RedisQueue:
    def __init__(self, name: str, redis: Redis):
        self.name = name
        self.redis = redis

    def push(self, x):
        return self.redis.rpush(self.name, x)

    def pop(self):
        return self.redis.lpop(self.name)


class TaskQueue(RedisQueue):
    def push(self, task: Task):
        return super().push(task.dumps())

    def pop(self):
        s = super().pop()
        if s is None:
            return
        return Task.loads(s)
