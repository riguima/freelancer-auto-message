from dataclasses import dataclass


@dataclass
class Project:
    url: str
    category: str
    name: str
    client_name: str


@dataclass
class Message:
    project: Project
    text: str
