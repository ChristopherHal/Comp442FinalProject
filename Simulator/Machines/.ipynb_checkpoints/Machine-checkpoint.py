from abc import ABC
import uuid

from Simulator.Tasks.Task import Task
from Simulator.Machines.Resources import Resources

class Machine(ABC):
    def __init__(self, resources: Resources, logger) -> None:
        self.resources: Resources = resources
        self.isWorking = False
        self.curWorkingTask: Task = None
        self.machineId = uuid.uuid3()
        self.logger = logger

    def getId(self) -> uuid.UUID:
        """Returns the id of the machine"""
        return self.machineId

    def isBusy(self) -> bool:
        """Returns if the current machine is busy"""
        return self.isWorking

    def execute(self) -> bool:
        """Execute a time step on the machine"""
        old_task = None
        if self.isWorking:
            self.isWorking = self.doWork()
            if not self.isWorking:
                old_task = self.curWorkingTask
                self.logger.log_finish(self, self.curWorkingTask)
                self.curWorkingTask = None
        return self.isWorking, old_task
    
    def loadTask(self, task) -> None:
        """ Loads a task on the machine which requires the task can be loaded"""
        assert self.canLoadTask(task)

        self.curWorkingTask = task
        self.isWorking = True
        self.logger.log_load_task(self, task)
    

    def canRunTask(self, task: Task) -> bool:
        """ Return if the inputted task can be run on the machine"""
        enough_mem = self.resources.memory >= task.getReq().memmory
        enough_cpus = self.resources.cpus >= task.getReq.cpus
        has_misc_req = True
        for mist_req in task.getReq().task_req:
            if mist_req not in self.resources.satified_req:
                has_misc_req = False
        return enough_cpus and enough_mem and has_misc_req

    def canLoadTask(self, task: Task) -> bool:
        """ Returns if the task can be run on the machine"""
        return self.canRunTask(task) and (not self.isWorking)

    def doWork(self) -> bool:
        """ Returns true if it is still working"""
        self.curWorkingTask.compTime = self.curWorkingTask.compTime - 1 * self.resources.power_level 
        if self.curWorkingTask.compTime <= 0:
            return False
        return True