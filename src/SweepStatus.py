import numpy as np
from queue import PriorityQueue

class SweepEvent:
    def __init__(self,  
                 point,
                 line1, 
                 line2, 
                 line1start = False, 
                 line1end = False,
                 line2start = False,
                 line2end = False,
                 pixelevent = False) -> None:
        self.point = point
        self.pixelevent = pixelevent
        self.line1 = line1
        self.line2 = line2
        self.line1start = line1start
        self.line1end = line1end
        self.line2start = line2start
        self.line2end = line2end
        
        
    


class SweepStatus:
    

    def __init__(self) -> None:
        self.events = PriorityQueue()
        self.status = {}
        
        
    
    def addevent(self, x:float, value):
        self.events.put(x, value)

    def nextevent(self):
        return self.events.get()
    
    def getfullstatus(self) -> list:
        return sorted(self.status)
    
    def getstatus(self, x):
        return self.status[x]
    
    def addstatus(self, x, value):
        self.status[x] = value

    def removestatus(self, x):
        return self.status.pop(x)

