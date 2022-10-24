import abc
from dataclasses import dataclass

@dataclass
class Resources(abc):
    """Class for keeping track of resources"""
    cpu: int = 1
    memmory: int = 8
    satified_req: list = []