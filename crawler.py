import sys
import random
import os
import time
import requests
from bs4 import BeautifulSoup

#https://github.com/Surbowl/azlinzi-crawler
#2020-1-31

#Time interval of crawler
sleepTime = 0
#Connect & read timeout
timeOut = (10, 60)
#User-Agent list
ua_list = [
            {"User-Agent":"Opera/9.27 (Windows NT 5.2; U; zh-cn)"},
            {"User-Agent":"Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"},
            {"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; 360se)"},
            {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"},
            {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"},
            {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        ]

if __name__ == "__main__":
    #Process input parameters
    argvLen = len(sys.argv)
    if(argvLen < 2):
        print("Please input parameters")
        print("crawler.py [uri]")
        print("crawler.py [uri] [save_path]")
    else:
        #The uri you want to crawl
        uri = sys.argv[1]
        if(argvLen < 3):
            #Default save path
            filePath = sys.path[0] + "\\azlinzi"
        else:
            #Param save path
            filePath = sys.argv[2]
        print("Start")
        print("Uri:%s"%uri)
        print("File path:%s"%filePath)

        #Get html page
        response = requests.get(uri, headers = random.choice(ua_list), timeout = timeOut)
        if(response.status_code == 200):
            #Find all images
            soup = BeautifulSoup(response.content, "lxml")
            soup = soup.find("div", class_="tiled-gallery")
            soup = soup.find_all("img")
            
            total = len(soup)
            if(total > 0):
                print("There are %d pictures, please wait a moment..."%total)
                #Make dirs
                if not os.path.exists(filePath):
                    os.makedirs(filePath)
                #Start crawling for images
                number = 1
                for imgHtml in soup:
                    time.sleep(sleepTime)
                    print("%d/%d"%(number, total), end='\t')
                    #Get image src
                    imgSrc = imgHtml.get("data-orig-file")
                    fileName = imgSrc.split('/')[-1]
                    print(imgSrc, end='\t')
                    try:
                        #Get image file
                        imgFile = requests.get(imgSrc, headers = random.choice(ua_list), timeout = timeOut).content
                        #Save image file
                        with open(filePath + "\\" + fileName, 'wb') as f:
                            f.write(imgFile)
                        print("Succeed")
                    except:
                        print("Fail")
                    number = number + 1
            else:
                 print("No pictures found")       
            print("Finish")
        else:
            print("Websites inaccessible")
