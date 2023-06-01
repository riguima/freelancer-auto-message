from dataclasses import dataclass


@dataclass
class MessageSent:
    url: str
    account_name: str
    id: int = None
