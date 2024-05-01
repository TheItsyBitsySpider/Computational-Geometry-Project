import numpy as np
from src.SweepStatus import SweepStatus, SweepEvent, SweepEntry
from queue import LifoQueue
from math import inf
import cv2

class Rasterizer:

    def __init__(self, triangles, colors, resx:int = 640, resy:int=480, skybox = [255,255,255]) -> None:
        self.colors = colors
        self.resx = resx
        self.resy = resy
        self.background = skybox
        self.triangles = triangles
        # TODO: Make sure there's no points vertical to one another
        # TODO: Sort each triangle internally by x point value
        


    def setlinesandplanes(self):
        for i in range(len(self.triangles)):
            #print(type(self.triangles[i]))
            self.triangles[i] = sorted(np.array(self.triangles[i]), key=lambda tri: tri[0])
        #print(self.triangles)
        # generate lines
        # Lines are stored in the format [AB, AC, BC]
        self.lines = np.zeros((len(self.triangles), 3, 2, 3))
        for i, triangle in enumerate(self.triangles):
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
        self.planes = np.zeros((len(self.triangles), 4))
        for i, triangle in enumerate(self.triangles):
            self.planes[i,0:3] = np.cross(self.lines[i,0,1], self.lines[i,1,1])
            self.planes[i,3] = -sum(triangle[1] * self.planes[i,0:3])


        #print(self.lines)
        #print(self.planes)
        pass


    def rasterize(self) -> np.ndarray:
        self.setlinesandplanes()
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
            x:np.float128 = 10*i/self.resx
            self.sweepline.addevent(
                x, 
                SweepEvent(
                    i,
                    pixelevent=True
                )
                )


        # Sweep the space & print
        screen = np.full((self.resy, self.resx, 3), 255, dtype=np.uint8)
        
        screen[:,:] = self.background
        while not self.sweepline.emptyqueue():
            event = self.sweepline.nextevent() # event is (x value, SweepEvent)
            if event[1].pixelevent:
                # Write the current pixel at sweep to the screen
                # This technically makes this part of the algorithm O(nwlogn+nwh)
                x = event[0]
                status = self.sweepline.getfullstatus(event[0])
                if status == []:
                    continue #if the status is empty, leave column blank
                activetriangles = {}
                
                nexttriangleindex = 0
                nexty = status[0].line[0,1] + x * status[0].line[1,1]
                
                for y in range(self.resy):
                    while y*10/self.resy >= nexty:
                        if status[nexttriangleindex].triangle in activetriangles.keys():
                            try:
                                activetriangles.pop(status[nexttriangleindex].triangle)
                            except:
                                pass
                        else:
                            activetriangles[status[nexttriangleindex].triangle] = status[nexttriangleindex]
                        nexttriangleindex += 1
                        if nexttriangleindex >= len(status):
                            nexttriangleindex -= 1
                            nexty = inf
                            
                            break
                        nexty = status[nexttriangleindex].line[0,1] + x * status[nexttriangleindex].line[1,1]

                    if activetriangles == {}:
                        screen[y, int(x*self.resx//10)] = self.background
                        continue # escape case for empty cell

                    pixelheight = -inf
                    for t in activetriangles.items():
                        
                        # ax + by + cz + d = 0
                        # (- ax - by - d)/c =z
                        plane = self.planes[t[1].triangle]
                        h = (-plane[0]*x - plane[1]*y*10/self.resy - plane[3])/plane[2]
                        if h > pixelheight:
                            pixelheight=h
                            screen[y, int(x*self.resx//10)] = self.colors[t[1].triangle]
                
                #cv2.imshow("Rasterization", screen[::-1])
                
            else:
                # Update Sweepline status
                # TODO: Add subfunctions for determining line intersections
                #print("{} of length {}".format(self.sweepline.getfullstatus(event[0]), len(self.sweepline.getfullstatus(event[0]))))
                line1 = self.lines[event[1].line1[0], event[1].line1[1]]
                line2 = self.lines[event[1].line2[0], event[1].line2[1]]
                if event[1].line1start:
                    #print("Adding line 1")
                    self.sweepline.addstatus(SweepEntry(
                        line=line1,
                        lineindex=event[1].line1,
                        triangleindex=event[1].point[0],
                        # If either this is the first node or it's a continuation of a top line, this is a top line
                        
                        # A line is a top line if either it is the top line at the start or is the point with higher slope leading to it
                        topline= True if event[1].line2start and line1[1,1] > line2[1,1] else (self.lines[event[1].point[0],0,1,2] > self.lines[event[1].point[0],1,1,2]) == (event[1].point[1]==1) and event[1].point[1] != 0
                        ))
                    
                else:
                    #print("Removing line 1")
                    self.sweepline.removestatus(event[1].line1)
                if event[1].line2start:
                    #print("Adding line 2")
                    self.sweepline.addstatus(SweepEntry(
                        line=line2,
                        lineindex=event[1].line2,
                        triangleindex=event[1].point[0],
                        # If either this is the first node or it's a continuation of a top line, this is a top line
                        
                        # A line is a top line if either it is the top line at the start or is the point with higher slope leading to it
                        topline= True if event[1].line1start and line1[1,1] < line2[1,1] else (self.lines[event[1].point[0],0,1,2] > self.lines[event[1].point[0],1,1,2]) == (event[1].point[1]==1) and event[1].point[1] != 0
                        ))
                else:
                    #print("Removing line 2")
                    self.sweepline.removestatus(event[1].line2)
                # TODO: Finish the new line processes
                
        #print(self.sweepline.getfullstatus(event[0]))
        return screen
        

    def rotate(self, rotationmatrix):
        if len(rotationmatrix) != 3 or len(rotationmatrix[0]) != 3:
            return False
        
        for i, tri in enumerate(self.triangles):
            for j in range(3):
                self.triangles[i,j,0] -= 5.
                self.triangles[i,j,1] -= 5.
                self.triangles[i,j] = np.matmul(rotationmatrix, self.triangles[i,j])
                self.triangles[i,j,0] += 5.
                self.triangles[i,j,1] += 5.
        return True