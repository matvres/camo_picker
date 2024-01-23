from sklearn.cluster import KMeans
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import sys
import os
import platform
import json
import camogen

if (platform.system() == "Windows"):
    path = ".\\webpage\\public\\images\\"
    splt = sys.argv[1].split('\\')
else:
    path = "./webpage/public/images/"
    splt = sys.argv[1].split('/')

img = path + splt[len(splt) - 1]


# pretvorba v grayscale ce potrebujemo:
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# funckija za pretvorbo RGB barv v HEXCODES
def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


# funkcija, ki prebere sliko s knjiznico CV2
def get_image(image_path):
    image = cv2.imread(image_path)
    # print("The type of this input is {}".format(type(image)))
    # print("Shape: {}".format(image.shape))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


# funkcija ki vrne RGB barve
def get_colors(image, number_of_colors, show_chart):
    # resize glede na veliksot dodaj

    modified_image = cv2.resize(image, (200, 200), interpolation=cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

    clf = KMeans(n_clusters=number_of_colors)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)
    # sort to ensure correct color percentage
    counts = dict(sorted(counts.items()))

    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    cnts = []
    for i in counts.keys():
        cnts.append(counts[i])

    print(ordered_colors)
    print(hex_colors)
    print(cnts)
    print(counts.values())
    print(list(counts.values()))

    return rgb_colors


# print(get_colors(get_image(img), 10, True))
get_colors(get_image(img), 8, True)
