from src.PlaneSweepRasterizer import Rasterizer
from src.display import Screen
import numpy as np
if __name__=="__main__":
    # kx3x3 matrix of triangles and their points
    triangles = np.array([
        [[0,0,0], [1,0,0], [2,1,1]]
    ])

    raster = Rasterizer(triangles)
    disp = Screen()
    print(raster)
    out = raster.rasterize()
    print(out)
    disp.display(out)