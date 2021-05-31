import matplotlib.image as mpimg
import numpy as np

# Output: A numpy array
# Reads an image and return a numpy array of the image
def getImage(path):
    return mpimg.imread(path)