import cv2
import numpy as np
class Screen():
    def __init__(self) -> None:
        pass


    def display(self, img:np.ndarray, short=False):
        # cv2 flips the image and is bgr
        cv2.imshow("Rasterization", img[::-1,:,::-1])
        if short:
            cv2.waitKey(1)
        else:
            cv2.waitKey(100000)

    