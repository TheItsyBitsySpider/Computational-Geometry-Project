import numpy as np
from queue import PriorityQueue
from dataclasses import dataclass

@dataclass(order=False)
class SweepEvent:
    def __init__(self,  
                 point,         # Index of the point in the triangle array
                 line1 = [-1, -1],    # Index of line 1
                 line2 = [-1, -1],    # Index of line 2
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
        
class SweepEntry:
    def __init__(
            self, 
            line,
            lineindex, 
            triangleindex,
            topline
        ) -> None:

        self.line = line
        self.lineindex = lineindex
        self.triangle = triangleindex
        self.topline = topline
        
    


class SweepStatus:
    

    def __init__(self) -> None:
        self.events = PriorityQueue()
        self.status = []
        
        
    
    def addevent(self, x:float, value:SweepEvent) -> None:
        self.events.put((x, value))

    def nextevent(self) -> SweepEvent:
        return self.events.get()
    

    def getfullstatus(self, x:float) -> list[SweepEntry]:
        # Sort the list by y value at the given x
        ret = self.status.sort(key=lambda entry: (entry.line[1,2] * x) + entry.line[0,2])
        return [] if ret == None else ret
    
    #def getstatus(self, x) -> list: # Returns the line? And maybe what triangle it's attached to?
    #    return self.status[x]
    
    def addstatus(self, value:SweepEntry) -> None:
        self.status.insert(value)

    def removestatus(self, x) -> SweepEvent:
        return self.status.pop(x)
    
    def emptyqueue(self) -> bool:
        return self.events.empty()
    

