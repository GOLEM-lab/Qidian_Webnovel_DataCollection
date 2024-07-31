import os
import re
import json
import time
import requests
import numpy as np
import pandas as pd
from lxml import html
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from datetime import datetime


def get_WebnovelFreeChapterIds(bookUrl,bookId):
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,th;q=0.6,tr;q=0.5,nl;q=0.4",
        "cookie": "_csrfToken=4dbce8fb-ea3d-49d8-936a-b82dac7812cf; webnovel_uuid=1721082484_17363682; webnovel-content-language=en; webnovel-language=en; Hm_lvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721082488; HMACCOUNT=66714B21096099E3; _gid=GA1.2.826710995.1721082489; dontneedgoogleonetap=1; para-comment-tip-show=1; AMP_TOKEN=%24NOT_FOUND; Hm_lpvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721121337; _ga=GA1.1.610756682.1721082489; _ga_PH6KHFG28N=GS1.1.1721121332.3.1.1721122197.60.0.0",
        "priority": "u=1, i",
        "referer": "https://www.webnovel.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    url = bookUrl + '/catalog'
    response = requests.request("GET", url, headers=headers)
    soup = bs(response.text,'html')
    volumes = soup.find_all('div',{'class':'volume-item'})
    #finding the chapterIds 
    allLinks = []
    for i in range(len(volumes)):
        allLinks = allLinks +volumes[i].find_all('li')

    #remove non free chapters
    allFreeChapterIds = [link['data-cid'] for link in allLinks if not link.find_all('svg')]
    allFreeChapterTitles = [link.find_all('a')[0]['title'] for link in allLinks if not link.find_all('svg')]
    df = pd.DataFrame({'chapterId':allFreeChapterIds,'chapterTitle':allFreeChapterTitles})
    df.to_csv('data/webnovelFreeChapterIds/' + bookId + '.csv',index=False)



if __name__ == "__main__":
    bookList = pd.read_csv('data/bookList.csv',dtype={'webnovelBookId':'string'})
    bookList = bookList.dropna(subset=['webnovelUrl'])
    for i, book in bookList.iterrows():
        print(i)
        bookId = book['webnovelBookId']
        bookUrl = book['webnovelUrl']
        get_WebnovelFreeChapterIds(bookUrl,bookId)