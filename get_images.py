import requests
import os
from bs4 import BeautifulSoup
import time
import random
import os.path
import urllib.parse
from selenium import webdriver

headers = {
    "Accept": "image/webp,*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "sl,en-GB;q=0.7,en;q=0.3",
    "Dnt": "1",
    "Host": "www.camopedia.org",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0",
  }



def getLines(line):
    # open pic links txt file
    country = line.split("=")
    file = open("./CamoPicker/img_links/" + country[1] + ".txt", "r")
    lines = file.readlines()
    file.close()
    return lines

def createPicDirAndReturnPath(line):
    country = line.split("=")
    dir = country[1]
    dir = dir.replace("...", "").replace(".", "").replace("/", "").replace(":", "").replace("*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace("|", "").replace("\n", "")
    dirPic = "./CamoPicker/" + dir
    #dirPic = "./CamoPicker/" + "images/" + dir#remove
    if not os.path.isdir(dirPic):
        os.mkdir(dirPic)
    return dirPic

def getPicName(pic):
    picName = pic.split("/")
    return picName[len(picName)-1].replace("/", "").replace(":", "").replace("*", "").replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace("|", "").replace("\n", "")

def isPicValid(pic):
    extension = pic.split(".")
    extension = extension[len(extension)-1].replace("\n", "")
    return extension == "jpg"

def getPicCompleteUrl(pic):
    baseUrl = "https://www.camopedia.org"
    return baseUrl + pic.replace("\n", "")

def countryPicturesDownload(line, listOfPics):
    #get image links
    lines = getLines(line)
    #create and return directory path
    dirPic = createPicDirAndReturnPath(line)
    for pic in lines:
        picName = getPicName(pic)
        if isPicValid(pic):
            print("--ValidPic: " + picName)
            url = getPicCompleteUrl(pic)
            #listOfPics.write(dirPic + "/" + picName + "\n")#remove
            #"""
            try:
                if os.path.isfile(dirPic + "/" + picName):
                    print("--" + picName + " IMAGE Alredy EXISTS, SKIPPING")
                else:
                    img = requests.get(url, headers=headers)
                    with open(dirPic + "/" + picName, "wb") as file_img:
                        file_img.write(img.content)
                        file_img.close()
                    print("--" + picName + " IMAGE DOWNLOADED")
                    listOfPics.write(dirPic + "/" + picName + "\n")
            except Exception as ex2:
                print("--!!! Exception !!!")
                print(ex2)
            #"""
        else:
            print("--NonValid IMAGE, SKIPPING")


#start program

#open links.txt file
file = open("./CamoPicker/links.txt", "r")
lines = file.readlines()
file.close()
#go through every link
for line in lines:
    # file with all pics
    listOfPics = open("./CamoPicker/listOfPics.txt", "a")#w+ does not append
    print("Country: " + line)
    countryPicturesDownload(line, listOfPics)
    time.sleep(3 + random.randint(3, 9))#comment if not dl
    # close
    listOfPics.close()#close every loop, bc. if it crashes
