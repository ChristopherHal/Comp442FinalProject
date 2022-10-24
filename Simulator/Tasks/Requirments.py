import abc
from dataclasses import dataclass

@dataclass
class Requirements(abc):
    """Class for keeping track of requirments"""
    cpu: int = 1
    memmory: int = 8
    task_req: list = []
