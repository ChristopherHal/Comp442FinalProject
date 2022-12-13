from dataclasses import dataclass

@dataclass
class Requirements:
    """Class for keeping track of requirments"""
    cpus: int = 1
    memory: int = 8
    task_req: tuple = ()
