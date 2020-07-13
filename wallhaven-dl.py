########################################################
#        Program to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                                                      #
#                  Dated- 26 June 2016                 #
#                 Update - 11 June 2019                #
########################################################

import os
import getpass
import re
import requests
import tqdm
import time
import urllib
import json

os.makedirs('Wallhaven', exist_ok=True)
BASEURL=""
cookies=dict()

global APIKEY
APIKEY = "YOURAPIKEY"

def artist():
    global BASEURL
    print('''
    ****************************************************************
                            Category Codes

    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallapapers only.
    ga      - For 'General' and 'Anime' wallapapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ').lower()
    ctags = {'all':'111', 'anime':'010', 'general':'100', 'people':'001', 'ga':'110', 'gp':'101' }
    ctag = ctags[ccode]

    print('''
    ****************************************************************
                            Purity Codes

    sfw     - For 'Safe For Work'
    sketchy - For 'Sketchy'
    nsfw    - For 'Not Safe For Work'
    ws      - For 'SFW' and 'Sketchy'
    wn      - For 'SFW' and 'NSFW'
    sn      - For 'Sketchy' and 'NSFW'
    all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    pcode = input('Enter Purity: ')
    ptags = {'sfw':'100', 'sketchy':'010', 'nsfw':'001', 'ws':'110', 'wn':'101', 'sn':'011', 'all':'111'}
    ptag = ptags[pcode]

    sortingType = input('''Choose how you want to sort the images:

    Enter "relevance" for downloading wallpapers sorted by relevance
    Enter "random" for downloading wallpapers randomly
    Enter "date_added" for downloading wallpapers sorted by date added
    Enter "views" for downloading wallpapers sorted by number of views
    Enter "favorites" for downloading wallpapers sorted by favorites
    Enter "toplist" for downloading wallpapers sorted by toplist
    Enter "toplist-beta" for downloading wallpapers sorted  by toplist beta

    Enter choice: ''').lower()
    while sortingType not in ['relevance', 'random', 'date_added','views', 'favorites', 'toplist','toplist-beta']:
        if sortingType != None:
            print('You entered an incorrect value.')
        sortingType = input('Enter choice: ')

    sortingOrder = input('''Choose the sorting order of your images:

    Enter "asc" for downloading wallpapers sin ascending order
    Enter "desc" for downloading wallpapers in descending order

    Enter choice: ''').lower()
    while sortingOrder not in ['asc', 'desc']:
        if sortingOrder != None:
            print('You entered an incorrect value.')
        sortingOrder = input('Enter choice: ')



    artistId = input('Enter artist id: ')

    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + '&q=id:' + artistId + "&categories=" +\
        ctag + '&purity=' + ptag + '&sorting=' + sortingType + '&order=' + sortingOrder + '&page='


def category():
    global BASEURL
    print('''
    ****************************************************************
                            Category Codes

    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallapapers only.
    ga      - For 'General' and 'Anime' wallapapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    ccode = input('Enter Category: ').lower()
    ctags = {'all':'111', 'anime':'010', 'general':'100', 'people':'001', 'ga':'110', 'gp':'101' }
    ctag = ctags[ccode]

    print('''
    ****************************************************************
                            Purity Codes

    sfw     - For 'Safe For Work'
    sketchy - For 'Sketchy'
    nsfw    - For 'Not Safe For Work'
    ws      - For 'SFW' and 'Sketchy'
    wn      - For 'SFW' and 'NSFW'
    sn      - For 'Sketchy' and 'NSFW'
    all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    pcode = input('Enter Purity: ')
    ptags = {'sfw':'100', 'sketchy':'010', 'nsfw':'001', 'ws':'110', 'wn':'101', 'sn':'011', 'all':'111'}
    ptag = ptags[pcode]

    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + "&categories=" +\
        ctag + '&purity=' + ptag + '&page='

def latest():
    global BASEURL
    print('Downloading latest')
    topListRange = '1M'
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + '&topRange=' +\
    topListRange + '&sorting=toplist&page='

def search():
    global BASEURL
    query = input('Enter search query: ')
    BASEURL = 'https://wallhaven.cc/api/v1/search?apikey=' + APIKEY + '&q=' + \
        urllib.parse.quote_plus(query) + '&page='

def downloadPage(pageId, totalImage):
    url = BASEURL + str(pageId)
    urlreq = requests.get(url, cookies=cookies)
    pagesImages = json.loads(urlreq.content);
    pageData = pagesImages["data"]

    for i in range(len(pageData)):
        currentImage = (((pageId - 1) * 24) + (i + 1))

        url = pageData[i]["path"]
        
        filename = os.path.basename(url)
        osPath = os.path.join('Wallhaven', filename)
        if not os.path.exists(osPath):
            imgreq = requests.get(url, cookies=cookies)
            if imgreq.status_code == 200:
                print("Downloading : %s - %s / %s" % (filename, currentImage , totalImage))
                with open(osPath, 'ab') as imageFile:
                    for chunk in imgreq.iter_content(1024):
                        imageFile.write(chunk)
            elif (imgreq.status_code != 403 and imgreq.status_code != 404):
                print("Unable to download %s - %s / %s" % (filename, currentImage , totalImage))
        else:
            print("%s already exist - %s / %s" % (filename, currentImage , totalImage))

def main():
    Choice = input('''Choose how you want to download the image:

    Enter "category" for downloading wallpapers from specified categories
    Enter "latest" for downloading latest wallpapers
    Enter "search" for downloading wallpapers from search
    Enter "artist" for downloading wallpapers from artist

    Enter choice: ''').lower()
    while Choice not in ['category', 'latest', 'search','artist']:
        if Choice != None:
            print('You entered an incorrect value.')
        choice = input('Enter choice: ')

    if Choice == 'artist':
        artist()
    elif Choice == 'category':
        category()
    elif Choice == 'latest':
        latest()
    elif Choice == 'search':
        search()

    pgid = int(input('How Many pages you want to Download: '))
    totalImageToDownload = str(24 * pgid)
    print('Number of Wallpapers to Download: ' + totalImageToDownload)
    for j in range(1, pgid + 1):
        downloadPage(j, totalImageToDownload)

if __name__ == '__main__':
    main()
