import numpy as np
from src.SweepStatus import SweepStatus, SweepEvent, SweepEntry
from queue import LifoQueue

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
                    point = [i,0],
                    line1 = [i,0],
                    line2 = [i,1],
                    line1start= True,
                    line2start= True
            ))

            self.sweepline.addevent(
                triangle[1,0],
                SweepEvent(
                    point = [i,1],
                    line1 = [i,0],
                    line2 = [i,2],
                    line1end= True,
                    line2start= True
            ))

            self.sweepline.addevent(
                triangle[2,0],
                SweepEvent(
                    point=[i,2],
                    line1=[i,1],
                    line2=[i,2],
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
                colorstack = LifoQueue()
                colorstack.put([255, 255, 255])
                #print("PixelEvent at {}".format(i))
                #if len(status) == 0:
                #    print("Empty PixelEvent at {}".format(event[0]))
                for line in reversed(status):
                    # fill all points below an area with the triangle's color
                    if line.topline == True: #TODO: Chance this to an array given with the triangles
                        colorstack.put([40,40,40])
                    else:
                        colorstack.get()
                    #print("Writing to ({}, {})".format(int((self.resx*line.line[1,2]) + line.line[0,2])*self.resy//10, int(event[0]*self.resx//10)))
                    #print(line.line)
                    color = colorstack.get()
                    for y in range(int((event[0]*line.line[1,1] + line.line[0,1])*self.resy/10.), -1, -1):
                        screen[y, int(event[0]*self.resx//10)] = color
                        #print("Writing to ({}, {})".format(y, int(event[0]*self.resx//10)))
                    colorstack.put(color)
                    #screen[:int((event[0]*line.line[1,2]) + line.line[0,2])*self.resy//10, int(event[0]*self.resx//10)].fill(40)
                    pass
                
                
            else:
                # Update Sweepline status
                # TODO: Add subfunctions for determining line intersections
                print("{} of length {}".format(self.sweepline.getfullstatus(event[0]), len(self.sweepline.getfullstatus(event[0]))))
                line1 = self.lines[event[1].line1[0], event[1].line1[1]]
                line2 = self.lines[event[1].line2[0], event[1].line2[1]]
                if event[1].line1start:
                    print("Adding line 1")
                    self.sweepline.addstatus(SweepEntry(
                        line=line1,
                        lineindex=event[1].line1,
                        triangleindex=event[1].point[0],
                        # If either this is the first node or it's a continuation of a top line, this is a top line
                        
                        # A line is a top line if either it is the top line at the start or is the point with higher slope leading to it
                        topline= True if event[1].line2start and line1[1,1] > line2[1,1] else (self.lines[event[1].point[0],0,1,2] > self.lines[event[1].point[0],1,1,2]) == (event[1].point[1]==1) and event[1].point[1] != 0
                        ))
                    
                else:
                    print("Removing line 1")
                    self.sweepline.removestatus(event[1].line1)
                if event[1].line2start:
                    print("Adding line 2")
                    self.sweepline.addstatus(SweepEntry(
                        line=line2,
                        lineindex=event[1].line2,
                        triangleindex=event[1].point[0],
                        # If either this is the first node or it's a continuation of a top line, this is a top line
                        
                        # A line is a top line if either it is the top line at the start or is the point with higher slope leading to it
                        topline= True if event[1].line1start and line1[1,1] < line2[1,1] else (self.lines[event[1].point[0],0,1,2] > self.lines[event[1].point[0],1,1,2]) == (event[1].point[1]==1) and event[1].point[1] != 0
                        ))
                else:
                    print("Removing line 2")
                    self.sweepline.removestatus(event[1].line2)
                # TODO: Finish the new line processes
                
        print(self.sweepline.getfullstatus(event[0]))
        return screen
        
        