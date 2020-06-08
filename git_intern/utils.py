import numpy as np
import cv2
import matplotlib.pyplot as plt

from PIL import Image


def load_image(path):
    img=cv2.imread(path)
    resized = cv2.resize(img, (img.shape[1]//4,img.shape[0]//4),interpolation = cv2.INTER_CUBIC)
    im=cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)
    return im


def plot_sample(lr, sr):
    plt.figure(figsize=(20, 10))

    images = [lr, sr]
    titles = ['LR', f'SR (x{sr.shape[0] // lr.shape[0]})']

    for i, (img, title) in enumerate(zip(images, titles)):
        plt.subplot(1, 2, i+1)
        plt.imshow(img)
        plt.title(title)
        plt.xticks([])
        plt.yticks([])
    plt.show()
