import abc
from Simulator.Machines.Machine import Machine

class Logger(abc):
    """Class responsable for logging during run will be used for stat generation"""
    def __init__(self, machines: list[Machine]) -> None:
        self.machines = machines
