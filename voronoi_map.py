from numpy.lib.function_base import _median_dispatcher
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import sys
import os
import platform
import json
import random
import math
from PIL import Image

# funkcija za generiranje seedov
def generateSeeds(num_seeds, width, height, colors):

    seeds = []

    for i in range(0, num_seeds):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        c = random.randint(0, len(colors)-1)

        p = [x,y,colors[c]]

        seeds.append(p)

    return seeds


# funckija za generiranje voronoi mape
def generateVoronoiMapEuc(path, num_seeds, width, height, colors):

    seeds = generateSeeds(num_seeds, width, height, colors)
    data = prepareImage(width, height)

    for i in range(0,width):
        for j in range(0,height):

            min_distance = 999999
            min_index = 0

            for h in range(0,num_seeds-1):

                distance = calcEuclidean(i,j,seeds[h][0], seeds[h][1])

                if distance < min_distance:
                    min_distance = distance
                    min_index = h
            
            data[i,j] = seeds[min_index][2]
          
    img = Image.fromarray(data, 'RGB')
    img.save(path)

    return 0

# funckija za generiranje voronoi mape
def generateVoronoiMapMan(path, num_seeds, width, height, colors):

    seeds = generateSeeds(num_seeds, width, height, colors)
    data = prepareImage(width, height)

    for i in range(0,width):
        for j in range(0,height):
            min_distance = 999999
            min_index = 0
            for h in range(0,num_seeds-1):
                distance = calcManhattan(i,j,seeds[h][0], seeds[h][1])
                if distance < min_distance:
                    min_distance = distance
                    min_index = h
            data[i,j] = seeds[min_index][2]

    img = Image.fromarray(data, 'RGB')
    img.save(path)

    return img


# Create a 500x500x3 array of 8 bit unsigned integers
def prepareImage(width, height):
    data = np.zeros( (width,height,3), dtype=np.uint8 )

    return data

# funkcija za izračun evklidske razdalje
def calcEuclidean(x1, y1, x2, y2):
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))

# funkcija za izračun manhattanske razdalje
def calcManhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


colors = [
        [
          147.2355534926897,
          122.59572986771867,
          101.487816198654
        ],
        [
          210.0821986888555,
          196.6941502773573,
          163.89309127584482
        ],
        [
          66.2928684627575,
          61.31600633914434,
          71.26117274167981
        ],
        [
          106.99579293945473,
          135.6365465520395,
          104.87451984635084
        ],
        [
          130.33444511825354,
          105.42647058823546,
          84.66388720436612
        ],
        [
          172.60915689558914,
          161.20603015075386,
          129.50362925739807
        ]]
        

#generateVoronoiMapMan('.\\testvoroni.png',100,200,200,colors)

#generateVoronoiMapEuc('.\\testvoroni.png',100,200,200,colors)