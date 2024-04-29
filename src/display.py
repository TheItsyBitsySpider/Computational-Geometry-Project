import cv2
import numpy as np
class Screen():
    def __init__(self) -> None:
        pass


    def display(self, img:np.ndarray):
        cv2.imshow("Rasterization", img)
        cv2.waitKey(1)