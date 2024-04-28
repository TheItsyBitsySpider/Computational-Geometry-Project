import numpy as np
from src.SweepStatus import SweepStatus, SweepEvent
class Rasterizer:

    def __init__(self, triangles, resx:int = 640, resy:int=480) -> None:
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


    def rasterize(self):
        # Form the sweep plane
        self.sweepline = SweepStatus()
        for i, triangle in enumerate(self.triangles):
            self.sweepline.addevent(
                triangle[0,0],
                SweepEvent(
                    triangle[0],
                    [i,0],
                    [i,1],
                    line1start= True,
                    line2start= True
            ))

            self.sweepline.addevent(
                triangle[1,0],
                SweepEvent(
                    triangle[1],
                    [i,1],
                    [i,2],
                    line1end= True,
                    line2start= True
            ))

            self.sweepline.addevent(
                triangle[2,0],
                SweepEvent(
                    triangle[2],
                    [i,0],
                    [i,2],
                    line1end= True,
                    line2end= True
            ))


        # Sweep the space

        # print results
        pass