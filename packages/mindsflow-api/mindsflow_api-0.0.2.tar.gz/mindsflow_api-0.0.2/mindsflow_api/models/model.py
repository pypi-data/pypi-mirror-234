from typing import Optional
from .chat import Chat
from .history import History


class Event(dict):
    chat: Optional[Chat] = Chat()


class Context(dict):
    history: Optional[History] = History()
