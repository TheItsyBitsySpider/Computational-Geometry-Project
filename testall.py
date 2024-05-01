from src.PlaneSweepRasterizer import Rasterizer
from src.display import Screen
import numpy as np
from math import sin,cos
if __name__=="__main__":
    # kx3x3 matrix of triangles and their points
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

    raster = Rasterizer(triangles, colors, skybox=[200,200,200])
    disp = Screen()
    
    out = raster.rasterize()
    print(out.shape)
    disp.display(out, short=True)
    while(True):
        inp = input("Input rotation of form [x|y|z][+|-][integer], or 'quit' to quit\n")
        if inp == 'quit':
            break

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