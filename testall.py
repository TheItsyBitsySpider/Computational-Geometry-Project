from src.PlaneSweepRasterizer import Rasterizer
from src.display import Screen
import numpy as np
from math import sin,cos,pi
if __name__=="__main__":
    # kx3x3 matrix of triangles and their points
    #this is the original testing array, overwritten by the boat
    triangles = np.array([
        [[0,0,0], [4,0,0], [8,4,12]],
        [[1,0,0], [4,6,2], [7,0,4]],
        [[1,7,-1], [5,7,-1], [3,1,5]]
    ], dtype=float)

    colors = np.array([
        [255, 100, 180],
        [40, 40, 200],
        [40, 200, 40]
    ])

    # Boat!
    triangles = np.array([
        #floor
        [[2,0,0], [5,0,2], [5.01,0,-2]],
        [[8,0,0], [5,0,2], [5.01,0,-2]],
        
        # walls
        [[2,0,0], [1,2,0], [5,0,2]],
        [[5.01,0,2], [1,2,0], [5,2,3]],
        [[2,0,0], [1,2,0], [5,0,-2]],
        [[5.01,0,-2], [1,2,0], [5,2,-3]],

        [[8,0,0], [9,2,0], [5,0,2]],
        [[5.01,0,2], [9,2,0], [5,2,3]],
        [[8,0,0], [9,2,0], [5,0,-2]],
        [[5.01,0,-2], [9,2,0], [5,2,-3]],

        #mast

        [[4.6,0,0], [5,8,0],[5.4,0,0]],
        #sail
        [[2,3,0],[4.7,3,0],[5,8,0]],
        [[7.5,3,0],[5.3,3,0],[5,8,0]]
    ])

    colors = np.array([
        #floor
        [40,40,80],
        [40,40,80],

        #walls
        [40,40,120],
        [40,40,200],
        [40,40,120],
        [40,40,200],

        [40,40,120],
        [40,40,200],
        [40,40,120],
        [40,40,200],

        #mast
        [220,160,40],

        #sail
        [200,40,40],
        [200,40,40]
    ])

    raster = Rasterizer(triangles, colors, skybox=[200,200,200], resx=640, resy=480)
    disp = Screen()
    
    out = raster.rasterize()
    print(out.shape)
    disp.display(out, short=True)
    while(True):
        inp = input("Input rotation of form [x|y|z][+|-][integer], or 'quit' to quit\n")
        if inp == 'quit':
            break
        
        if inp == 'spin':
            t=.05
            for i in range(int(2*pi/0.05)):
                raster.rotate([
                        [cos(t), 0, sin(t)],
                        [0,     1,  0],
                        [-sin(t), 0, cos(t)]

                    ])
                disp.display(raster.rasterize(), True)
            continue

        try:
            t = float(inp[1:])
            if inp[0] == 'x':
                raster.rotate([
                    [1,0,      0],
                    [0,cos(t),-sin(t)],
                    [0,sin(t),cos(t)]

                ])
            if inp[0] == 'y':
                raster.rotate([
                    [cos(t), 0, sin(t)],
                    [0,     1,  0],
                    [-sin(t), 0, cos(t)]

                ])
            if inp[0] == 'z':
                raster.rotate([
                    [cos(t), -sin(t), 0],
                    [sin(t), cos(t), 0],
                    [0,     0,      1]
                ])

            

            out = raster.rasterize()
            disp.display(out, short=True)
        except:
            print("Invalid input, rotation discarded")

    
    print("Goodbye!")