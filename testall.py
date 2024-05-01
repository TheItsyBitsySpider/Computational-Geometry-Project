from src.PlaneSweepRasterizer import Rasterizer
from src.display import Screen
import numpy as np
if __name__=="__main__":
    # kx3x3 matrix of triangles and their points
    triangles = np.array([
        [[0,0,0], [4,0,0], [8,4,4]],
        [[0,0,0], [3,6,2], [6,0,4]],
        [[1,7,-1], [3,1,5], [5,7,-1]]
    ])

    colors = np.array([
        [255, 100, 180],
        [40, 40, 200],
        [40, 200, 40]
    ])

    raster = Rasterizer(triangles, colors, skybox=[200,200,200])
    disp = Screen()
    print(raster)
    out = raster.rasterize()
    print(out.shape)
    disp.display(out)