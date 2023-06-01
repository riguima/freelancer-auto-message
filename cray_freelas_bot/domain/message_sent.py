from dataclasses import dataclass


@dataclass
class MessageSent:
    url: str
    id: int = None
