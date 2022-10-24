import abc
import Requirments


class Task(abc):
    def __init__(self, taskId, requirments, compTime) -> None:
        """Constructor for a task requires and id"""
        self.taskId = taskId
        self.requirments = requirments
        self.compTime = compTime
    
    def getReq(self) -> Requirments:
        return self.requirments
    
    def getTimeLeft(self) -> int:
        """Get the amount of computation left"""
        return self.compTime


    def isDone(self) -> bool:
        return self.isDone
