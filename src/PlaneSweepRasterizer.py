import numpy as np
from src.SweepStatus import SweepStatus, SweepEvent, SweepEntry
class Rasterizer:

    def __init__(self, triangles, resx:int = 640, resy:int=480) -> None:
        self.resx = resx
        self.resy = resy
        # TODO: Make sure there's no points vertical to one another
        # TODO: Sort each triangle internally by x point value

        self.triangles = triangles
        # generate lines
        # Lines are stored in the format [AB, AC, BC]
        self.lines = np.zeros((len(triangles), 3, 2, 3))
        for i, triangle in enumerate(triangles):
            # Set the first line's slope, normalized to x
            self.lines[i][0][1] = (triangle[1] - triangle[0])/(triangle[1][0]-triangle[0][0])
            # Set the first line's position, normalized to x=0
            self.lines[i][0][0] = triangle[0] - (self.lines[i][0][1] * triangle[0][0])

            # Set the second line's slope, normalized to x
            self.lines[i][1][1] = (triangle[2] - triangle[0])/(triangle[2][0]-triangle[0][0])
            # Set the second line's position, normalized to x=0
            self.lines[i][1][0] = triangle[0] - (self.lines[i][1][1] * triangle[0][0])

            # Set the third line's slope, normalized to x
            self.lines[i][2][1] = (triangle[2] - triangle[1])/(triangle[2][0]-triangle[1][0])
            # Set the third line's position, normalized to x=0
            self.lines[i][2][0] = triangle[1] - (self.lines[i][2][1] * triangle[1][0])
        
        
        # generate planes
        self.planes = np.zeros((len(triangles), 4))
        for i, triangle in enumerate(triangles):
            self.planes[i,0:3] = np.cross(self.lines[i,0,1], self.lines[i,1,1])
            self.planes[i,3] = -sum((triangle[1]-triangle[0]) * triangle[0])


        print(self.lines)
        print(self.planes)
        pass


    def rasterize(self) -> np.ndarray:
        # Form the sweep plane
        self.sweepline = SweepStatus()
        for i, triangle in enumerate(self.triangles):
            self.sweepline.addevent(
                triangle[0,0],
                SweepEvent(
                    [i,0],
                    [i,0],
                    [i,1],
                    line1start= True,
                    line2start= True
            ))

            self.sweepline.addevent(
                triangle[1,0],
                SweepEvent(
                    [i,1],
                    [i,1],
                    [i,2],
                    line1end= True,
                    line2start= True
            ))

            self.sweepline.addevent(
                triangle[2,0],
                SweepEvent(
                    [i,2],
                    [i,0],
                    [i,2],
                    line1end= True,
                    line2end= True
            ))

        for i in range(self.resx):
            self.sweepline.addevent(
                10*i/self.resx, 
                SweepEvent(
                    i,
                    pixelevent=True
                )
                )


        # Sweep the space & print
        screen = np.full((self.resy, self.resx, 3), 255, dtype=np.uint8)
        while not self.sweepline.emptyqueue():
            event = self.sweepline.nextevent() # event is (x value, SweepEvent)
            if event[1].pixelevent:
                # Write the current pixel at sweep to the screen
                status = self.sweepline.getfullstatus(event[0])
                for line in reversed(status):
                    # fill all points below an area with the triangle's color
                    # TODO: Change 40,40,40 to triangle colors
                    screen[:((line.line[1,2]) + line.line[0,2])*self.resy/10., i] = [40,40,40]
                    pass
                
            else:
                # Update Sweepline status
                # TODO: Add subfunctions for determining line intersections
                line1 = self.lines[event[1].line1[0], event[1].line1[1]]
                line2 = self.lines[event[1].line2[0], event[1].line2[1]]
                if event[1].line1start:
                    self.sweepline.addstatus(SweepEntry(
                        line=line1,
                        lineindex=event[1].line1,
                        triangleindex=event[1].point[0],
                        # If either this is the first node or it's a continuation of a top line, this is a top line
                        # TODO: Fix the sweepline status not preserving top line status
                        topline= True if event[1].line2start and line1[1] > line2[1] else event[1].topline
                        ))
                # TODO: Finish the new line processes
                
                pass
        return screen
        
        