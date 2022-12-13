from dataclasses import dataclass

@dataclass
class Resources:
    """Class for keeping track of resources"""
    cpus: int = 1
    memory: int = 8
    satified_req: tuple = ()
    power_level: int = 1