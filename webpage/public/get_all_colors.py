from sklearn.cluster import KMeans
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import sys
import os
import platform
import json
from json import JSONEncoder

NUM_OF_COLORS = 10

class OurColor:
    def __init__(self, hex, rgb, percentage):
        self.hex = hex
        self.rgb = rgb
        self.percentage = percentage

class OurImage:
    def __init__(self, fileName, filePath, width, height, colors):
        self.fileName = fileName
        self.filePath = filePath
        self.family = ""
        self.width = width
        self.height = height
        self.colors = colors

class OurColorEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class OurImageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def get_IMG_C(image, number_of_colors):
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

    arrayColors = []

    #print(counts)

    cnts = []
    for i in counts.keys():
        cnts.append(counts[i])

    for i in range(len(rgb_colors)):
        c = OurColor(hex_colors[i], rgb_colors[i].tolist(), counts[i] / 40000.0)
        arrayColors.append(c)

    return arrayColors


#get json from file
tree_file = open("tree.json", "r")
tree = json.load(tree_file)
tree_file.close()

#DO NOT TOUCH
tree = tree[0]
tree = tree["contents"]
tree = tree[0]

imgs = []

#loop Directories
for directory in tree["contents"]:
    #print(directory["name"])
    for file in directory["contents"]:
        #print(file["name"])
        imgs.append(OurImage(file["name"], "/camos/images/" + directory["name"] + "/" + file["name"], 200, 200, get_IMG_C(get_image("./camos/images/" + directory["name"] + "/" + file["name"]), NUM_OF_COLORS)))
        #call color analyze



print(OurImageEncoder().encode(imgs))





