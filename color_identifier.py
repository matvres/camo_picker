from sklearn.cluster import KMeans
#import matplotlib.pyplot as plt, mpld3
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


NUM_OF_COLORS = 10

if(platform.system() == "Windows"):
    path = ".\\public\\images\\"
    splt = sys.argv[1].split('\\')
else:
    path = "./public/images/"#"./public/images/"#"./webpage/public/images/"
    splt = sys.argv[1].split('/')

img = path + splt[len(splt)-1]


# pretvorba v grayscale ce potrebujemo:
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# funckija za pretvorbo RGB barv v HEXCODES
def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

# funkcija, ki prebere sliko s knjiznico CV2
def get_image(image_path):
    image = cv2.imread(image_path)
    #print("The type of this input is {}".format(type(image)))
    #print("Shape: {}".format(image.shape))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def sort_colors_by_counts(cou, col, rgb):
    #print(cou)
    #print(col)

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


    #print(cou)
    #print(dic)
    chex = []
    for i in range(0, len(cou)):
        chex.append(dic[str(cou[i])])

    crgb = []
    for i in range(0, len(cou)):
        crgb.append((dic2[str(cou[i])]).tolist())#.tolist()

    result = []

    #print(cou)
    #print(chex)
    result.append(cou)
    result.append(chex)
    result.append(crgb)
    return result

# funkcija ki vrne RGB barve
def get_colors(image, number_of_colors, show_chart):
    
    # resize glede na veliksot dodaj

    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    
    counts = Counter(labels)
    # sort to ensure correct color percentage
    counts = dict(sorted(counts.items()))
    
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]


    if (show_chart):
        #f = plt.figure(figsize = (8, 6))
        #plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)

        if(platform.system() == "Windows"):
            pth = ".\\public\\files\\"
        else:
            pth = "./public/files/"


        #print(hex_colors)
        cnts = []
        for i in counts.keys():
            cnts.append(counts[i])

        #print(cnts)
        #print(ordered_colors)

        only6 = sort_colors_by_counts(cnts, hex_colors, rgb_colors)
        """
        hx = (only6[1])[:6]#(only6[1])[-6:]
        cc = (only6[0])[:6]#(only6[0])[-6:]
        ccrgb = (only6[2])[:6]
        """
        hx = (only6[1])[:6]#(only6[1])[-6:]
        cc = (only6[0])[:6]#(only6[0])[-6:]
        ccrgb = (only6[2])[:6]

        #print(hx)
        #print(ccrgb)

        #print(cc)
        #print(hx)

        temp = []
        temp.append(hx)#temp.append(hex_colors)
        temp.append(cc)#temp.append(cnts)
        temp.append(ccrgb)

        fl = open(pth + splt[len(splt)-1] + "_graf.txt", "w")
        fl.write(json.dumps(temp))
        fl.close()

        # Voronoi camo generation
        generateVoronoiMapEuc(pth + "v1" + splt[len(splt) - 1], 110, 300, 300, ccrgb)
        generateVoronoiMapMan(pth + "v2" + splt[len(splt) - 1], 110, 300, 300, ccrgb)


        #Generiranje kamuflaz - Camogen
        # Green Blots
        parameters = {'width': 700, 'height': 700, 'polygon_size': 200, 'color_bleed': 6,
                    'colors': hx,
                    'spots': {'amount': 20000, 'radius': {'min': 7, 'max': 14}, 'sampling_variation': 10}}

        image = camogen.generate(parameters)
        image.save(pth + splt[len(splt)-1])

        # Digital
        parameters = {'width': 700, 'height': 700, 'polygon_size': 150, 'color_bleed': 3,
                      'colors': hx,
                      'spots': {'amount': 500, 'radius': {'min': 20, 'max': 30}, 'sampling_variation': 20},
                      'pixelize': {'percentage': 1, 'sampling_variation': 20, 'density': {'x': 70, 'y': 50}}}

        image2 = camogen.generate(parameters)
        image2.save(pth + "2" + splt[len(splt) - 1])

        # Vodka
        parameters = {'width': 700, 'height': 700, 'polygon_size': 200, 'color_bleed': 0,
                      'colors': hx,
                      'spots': {'amount': 3000, 'radius': {'min': 30, 'max': 40}, 'sampling_variation': 10},
                      'pixelize': {'percentage': 0.75, 'sampling_variation': 10, 'density': {'x': 60, 'y': 100}}}

        image3 = camogen.generate(parameters)
        image3.save(pth + "3" + splt[len(splt) - 1])



    return rgb_colors


#print(get_colors(get_image(img), 10, True))
get_colors(get_image(img), NUM_OF_COLORS, True)



