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

    def nextevent(self) -> tuple[int, SweepEvent]:
        return self.events.get()
    


    def getfullstatus(self, x:float) -> list[SweepEntry]:
        return sorted(self.status, key=lambda entry: (entry.line[1,1] * x) + entry.line[0,1])
    
    #def getstatus(self, x) -> list: # Returns the line? And maybe what triangle it's attached to?
    #    return self.status[x]
    
    def addstatus(self, value:SweepEntry) -> None:
        self.status.append(value)

    def removestatus(self, x) -> SweepEvent:
        for i, stat in enumerate(self.status):
            if stat.lineindex == x:
                return self.status.pop(i)
        print("ERROR: Failed to find matching edge in SweepStatus.removestatus")
        return None
    
    def emptyqueue(self) -> bool:
        return self.events.empty()
    

