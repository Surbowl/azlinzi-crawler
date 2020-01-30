import random
import time
import urllib
import requests
from bs4 import BeautifulSoup

#The link you want to crawl
uri = "https://azlinzi.wordpress.com/2019/05/29/%e5%bf%a0%e9%8a%98-%e5%87%ba%e7%a7%9f%e7%94%b7%e5%ad%a9%e7%9a%84%e5%86%99%e7%9c%9f/"

#Save path
#If you save on disk C, you may need administrator privileges
filePath = "D:/azlinzi"

#Time interval of crawler
sleepTime = 0

#Connect & read timeout
timeOut=(10, 60)


ua_list = [
            {"User-Agent":"Opera/9.27 (Windows NT 5.2; U; zh-cn)"},
            {"User-Agent":"Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"},
            {"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; 360se)"},
            {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1"},
            {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"},
            {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        ]

if __name__ == "__main__":
    print("Start")
    response = requests.get(uri, headers = random.choice(ua_list))
    if(response.status_code == 200):
        soup = BeautifulSoup(response.content, "lxml")
        soup = soup.find("div", class_="tiled-gallery")
        soup = soup.find_all("img")

        total = len(soup)
        number = 1
        print("There are %d pictures"%total)

        for imgHtml in soup:
            time.sleep(sleepTime)
            print("%d/%d"%(number, total), end='\t')
            #Get img src
            imgSrc = imgHtml.get("data-orig-file")
            fileName = imgSrc.split('/')[-1]
            print(imgSrc, end='\t')
            try:
                #Get img
                imgFile = requests.get(imgSrc, headers = random.choice(ua_list), timeout = timeOut)
                #Save file
                with open(filePath + '/' + fileName,'wb') as f:
                    f.write(imgFile)
                print("Succeed")
            except:
                print("Fail")
            number = number + 1
    else:
        print("Websites inaccessible")