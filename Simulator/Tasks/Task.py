from abc import ABC
import uuid
from Simulator.Tasks.Requirements import Requirements

class Task(ABC):
    def __init__(self, requirments, compTime):
        """Constructor for a task requires and id"""
        self.taskId = uuid.uuid4()
        self.requirments = requirments
        self.compTime = compTime
    
    def getReq(self) -> Requirements:
        return self.requirments
    
    def getTimeLeft(self) -> int:
        """Get the amount of computation left"""
        return self.compTime


    def isDone(self) -> bool:
        return self.isDone
