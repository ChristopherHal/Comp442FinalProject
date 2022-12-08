from dataclasses import dataclass

@dataclass
class Resources:
    """Class for keeping track of resources"""
    cpu: int = 1
    memmory: int = 8
    satified_req: tuple = ()
    power_level: int = 1