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
from voronoi_map import generateVoronoiMapEuc, generateVoronoiMapMan

NUM_OF_COLORS = 3

if(platform.system() == "Windows"):
    print("Platform: Windows")
else:
    print("Platform: Linux")

def RGB2HEX(color):
    print("RGB2HEX")
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def get_image(image_path):
    print("Open Image test.jpg")
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def sort_colors_by_counts(cou, col, rgb):
    print("Sort Colors")
    dic = {}
    for i in range(0, len(cou)):
        dic[str(cou[i])] = col[i]

    dic2 = {}
    for i in range(0, len(cou)):
        dic2[str(cou[i])] = rgb[i]

    for i in range(1, len(cou)):
        key = cou[i]

        j = i - 1
        while j >= 0 and key > cou[j]:
            cou[j + 1] = cou[j]
            col[j + 1] = col[i]
            j -= 1
        cou[j + 1] = key

    chex = []
    for i in range(0, len(cou)):
        chex.append(dic[str(cou[i])])

    crgb = []
    for i in range(0, len(cou)):
        crgb.append((dic2[str(cou[i])]).tolist())

    result = []
    result.append(cou)
    result.append(chex)
    result.append(crgb)
    return result


def get_colors(image, number_of_colors, show_chart):
    print("Modify Image")
    modified_image = cv2.resize(image, (200, 200), interpolation=cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)
    print("KMeans")
    clf = KMeans(n_clusters=number_of_colors)
    labels = clf.fit_predict(modified_image)
    counts = Counter(labels)
    counts = dict(sorted(counts.items()))
    center_colors = clf.cluster_centers_
    print("Order Colors")
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (show_chart):

        cnts = []
        for i in counts.keys():
            cnts.append(counts[i])

        only6 = sort_colors_by_counts(cnts, hex_colors, rgb_colors)
        hx = (only6[1])[:2]
        cc = (only6[0])[:2]
        ccrgb = (only6[2])[:2]

        temp = []
        temp.append(hx)
        temp.append(cc)
        temp.append(ccrgb)

        print("Create test_graf.txt")
        fl = open("test_graf.txt", "w")
        fl.write(json.dumps(temp))
        fl.close()

        # Voronoi camo generation
        print("Create test_V1.jpg")
        generateVoronoiMapEuc("test_V1.jpg", 110, 300, 300, ccrgb)
        print("Create test_V2.jpg")
        generateVoronoiMapMan("test_V2.jpg", 110, 300, 300, ccrgb)

        # Generiranje kamuflaz - Camogen
        # Green Blots
        print("Create test_D1.jpg")
        parameters = {'width': 700, 'height': 700, 'polygon_size': 200, 'color_bleed': 6,
                      'colors': hx,
                      'spots': {'amount': 20000, 'radius': {'min': 7, 'max': 14}, 'sampling_variation': 10}}

        image = camogen.generate(parameters)
        image.save("test_D1.jpg")

        # Digital
        print("Create test_D2.jpg")
        parameters = {'width': 700, 'height': 700, 'polygon_size': 150, 'color_bleed': 3,
                      'colors': hx,
                      'spots': {'amount': 500, 'radius': {'min': 20, 'max': 30}, 'sampling_variation': 20},
                      'pixelize': {'percentage': 1, 'sampling_variation': 20, 'density': {'x': 70, 'y': 50}}}

        image2 = camogen.generate(parameters)
        image2.save("test_D2.jpg")

        # Vodka
        print("Create test_D3.jpg")
        parameters = {'width': 700, 'height': 700, 'polygon_size': 200, 'color_bleed': 0,
                      'colors': hx,
                      'spots': {'amount': 3000, 'radius': {'min': 30, 'max': 40}, 'sampling_variation': 10},
                      'pixelize': {'percentage': 0.75, 'sampling_variation': 10, 'density': {'x': 60, 'y': 100}}}

        image3 = camogen.generate(parameters)
        image3.save("test_D3.jpg")

    return rgb_colors


get_colors(get_image("test.jpg"), NUM_OF_COLORS, True)

print()
print()
print("=====================================")
print("CHECK FILES THAT: ")
print("test_graf.txt CONTAINS JSON")
print("Create test_V1.jpg IS A VALID IMAGE")
print("Create test_V2.jpg IS A VALID IMAGE")
print("Create test_D1.jpg IS A VALID IMAGE")
print("Create test_D1.jpg IS A VALID IMAGE")
print("Create test_D1.jpg IS A VALID IMAGE")