#!/usr/bin/python
import cv2
import glob
import numpy as np

class ImagePreprocessor:

    def __init__(self):
        pass

    @staticmethod
    def resize_images(directory):

        image_array = []
        print(directory)
        for img in glob.glob(directory+"/*.jpg"):
            image = cv2.imread(img, 0)
            r = 150.0 / image.shape[1]
            dim = (150, int(image.shape[0] * r))
            resize = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            r = 50.0 / image.shape[0]
            dim = (int(image.shape[1] * r), 50)
            resize = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            face = np.array(resize, 'uint8')
            image_array.append(face)

        return image_array


arr = ImagePreprocessor.resize_images("/home/patryk/Desktop/pictures")
cv2.imshow("Resized", arr[0])
print(type(arr))
cv2.waitKey(0)
cv2.destroyAllWindows()