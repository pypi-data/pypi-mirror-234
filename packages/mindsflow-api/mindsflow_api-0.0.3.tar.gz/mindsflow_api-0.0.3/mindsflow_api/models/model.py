from typing import Optional
from .chat import Chat
from .history import History


class Event(dict):
    chat: Optional[Chat] = Chat()


class Context(dict):
    history: Optional[History]

    def __init__(self, unique_key="", redis_url="redis://localhost:6379/0"):
        super().__init__()
        self.history = History(unique_key, redis_url)

    def get_serializable_dict(self):
        return {
            "unique_key": self.history.unique_key,
            "redis_url": self.history.redis_url,
        }

    @staticmethod
    def from_dict(data):
        return Context(data["unique_key"], data["redis_url"])
