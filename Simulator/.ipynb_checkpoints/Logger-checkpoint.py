from abc import ABC
import numpy as np
from Simulator.Machines.Machine import Machine
from Simulator.Tasks.Task import Task

class Logger(ABC):
    """Class responsable for logging during run will be used for stat generation"""
    def __init__(self) -> None:
        # self.machines = machines
        self.completed_tasks = []
        self.started_tasks = []
        self.cur_time = 0
    

    def log_finish(self, machine: Machine, task: Task):
        """Log the completion of a task"""
        self.completed_tasks.append((self.cur_time, machine.getId(), task))
    
    def log_load_task(self, machine: Machine, task: Task):
        """Log the start of the task"""
        self.started_tasks.append((self.cur_time, machine.getId(), task))
    
    

