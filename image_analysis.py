import numpy as np
from skimage import io, data
from skimage.exposure import histogram

img = io.imread("webpage/public/images/test16.png")

r_hvalues = histogram(img[:,:,0], nbins=8, source_range='dtype', normalize=False)
g_hvalues = histogram(img[:,:,1], nbins=8, source_range='dtype', normalize=False)
b_hvalues = histogram(img[:,:,2], nbins=8, source_range='dtype', normalize=False)

colors_rgb = []

print(r_hvalues[0])
print(g_hvalues[0])
print(b_hvalues[0])

print("Image size:")
print(img.shape)

print("Pixel na [0,0]:")
print(img[1,1,0])
print(img[1,1,1])
print(img[1,1,2])