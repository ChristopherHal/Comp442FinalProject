
import numpy as np
from Simulator.Logger import Logger 
from Simulator.Machines.Machine import Machine
from Simulator.Machines.Resources import Resources
from Simulator.Tasks.Task import Task
import heapq


class ResSim:
    def __init__(self,task_traffic: list[tuple[int, Task]], task_type_assigner, machine_configs: list[Resources], num_task_types: int, *, queue_len = 10):
        self.done = False
        self.task_traffic = list(task_traffic)
        heapq.heapify(self.task_traffic)
        self.task_type_assigner = task_type_assigner
        self.curTime = 0
        self.sysLogger = Logger()
        self.num_machines = len(machine_configs)
        self.max_que_len = queue_len
        self.machines = []
        for config in machine_configs:
            self.machines.append( Machine(config, self.sysLogger))
        self.num_task_types = num_task_types
        self.lookup_id_to_idx = {}
        self.current_task_status = np.zeros((num_task_types, queue_len))
        self.tasks_queue = [[] for x in range(num_task_types)]
        self.machines_status = np.zeros((self.num_machines))
        self.current_task_status = np.zeros([self.num_task_types, self.max_que_len])
        self.num_completed_tasks = 0
        # Create the machines due to the config

    
    def getActionDem(self):
        return (self.num_machines * self.num_task_types * self.max_que_len) + 1

    def getState(self):
        """Get the current state of the sim"""
        avaible_tasks = self.current_task_status
        machines_status = self.machines_status
        return np.concatenate([avaible_tasks.flatten(), machines_status], 0)
    

    def doAction(self, action) -> int:
        """Execute the action on the system"""

        #Parse the action

        # If it is a wait advance the time step

        reward = 0

        if action >= (self.num_machines * self.num_task_types * self.max_que_len):
            if (self.machines_status == 0).all() and not (self.task_traffic) and (self.current_task_status == 0).all():
                self.done = True
                return 0
            for i in range(len(self.machines)):
                    old_status = self.machines_status[i]
                    self.machines_status[i], task_finish = self.machines[i].execute()
                    if task_finish is not None:
                        # Reward for finishing a task
                        reward += self.task_type_assigner(task_finish.getReq()) * 10 
                        self.num_completed_tasks += 1
            self.curTime += 1
            self.sysLogger.cur_time += 1
            # Add new task to current_tasks
            while self.task_traffic and (self.task_traffic[0][0] <= self.curTime):
                task_to_add = heapq.heappop(self.task_traffic)[1]
                task_type = self.task_type_assigner(task_to_add.getReq())
                self.tasks_queue[task_type].append(task_to_add)
                if not (len(self.tasks_queue[task_type]) > self.max_que_len):
                    next_av = self.current_task_status[task_type].argmin()
                    assert self.current_task_status[task_type][next_av] == 0
                    self.current_task_status[task_type][next_av] = 1
            return reward

        machine_to_add_to = action  // (self.num_task_types * self.max_que_len)

        task_type = (action % (self.num_task_types * self.max_que_len)) // self.max_que_len

        task_num = (action % (self.num_task_types * self.max_que_len)) % self.max_que_len
        
#         print("Machine To Add: ", machine_to_add_to)
        
#         print("Task Type: ", task_type)
        
#         print("Task Num: ", task_num)
        

        # Handle the running of a specfic task and assigning to a machine

        # If it isnt a current task
        if not self.current_task_status[task_type][task_num]: 
            reward = -10        
        else:
            task = self.tasks_queue[task_type][0]
            if self.machines[machine_to_add_to].canLoadTask(task):
                self.machines[machine_to_add_to].loadTask(task)
                self.machines_status[machine_to_add_to] = 1
                self.tasks_queue[task_type].pop()
                # print("len queue: ", len(self.tasks_queue[task_type]))
                if len(self.tasks_queue[task_type]) < self.max_que_len:
                    # print("here")
                    self.current_task_status[task_type][task_num] = 0
                # reward = self.task_type_assigner(task.getReq()) * 10 
            else:
                reward = -10
        
        
        return reward