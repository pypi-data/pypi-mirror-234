from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class Command:
    entity: str
    payload: Dict[str, str]
    # def __init__(self, entity: str, payload: Optional[Dict[str, str]]):
    #     self.entity = entity
    #     self.payload = payload

    # def __repr__(self) -> str:
    #     return f"{self.__class__.__name__}(entity={self.entity}, payload={self.payload})"


@dataclass
class Edit(Command):
    ...


@dataclass
class Create(Command):
    ...


@dataclass
class Update(Command):
    ...


@dataclass
class Complete(Command):
    ...


@dataclass
class Start(Command):
    ...


@dataclass
class Create(Command):
    ...


@dataclass
class List(Command):
    ...


@dataclass
class Show(Command):
    ...


@dataclass
class Get(Command):
    ...


@dataclass
class Collaborate(Command):
    ...


@dataclass
class Track(Command):
    ...


@dataclass
class Tag(Command):
    ...


@dataclass
class Add(Command):
    ...


@dataclass
class Note(Command):
    ...


@dataclass
class Comment(Command):
    ...


@dataclass
class Delete(Command):
    ...


@dataclass
class Connect(Command):
    ...


@dataclass
class Report(Command):
    ...
