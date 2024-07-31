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



def get_Content(bookId,chapterId):
    url = "https://www.webnovel.com/go/pcm/chapter/getContent"

    querystring = {"_csrfToken":"4dbce8fb-ea3d-49d8-936a-b82dac7812cf","_fsae":"0","bookId":bookId,"chapterId":chapterId,"encryptType":"3","font":"Merriweather","_":"1721162916456"}

    payload = ""
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,th;q=0.6,tr;q=0.5,nl;q=0.4",
        "cookie": "_csrfToken=4dbce8fb-ea3d-49d8-936a-b82dac7812cf; webnovel_uuid=1721082484_17363682; webnovel-content-language=en; webnovel-language=en; _gid=GA1.2.826710995.1721082489; dontneedgoogleonetap=1; para-comment-tip-show=1; Hm_lvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721082488,1721141260,1721156823; HMACCOUNT=66714B21096099E3; AMP_TOKEN=%24NOT_FOUND; _gat=1; x-waf-captcha-referer=https%3A%2F%2Fwww.webnovel.com%2Fbook%2Fi-have-a-mansion-in-the-post-apocalyptic-world_7143532406000605; Hm_lpvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721162907; _ga=GA1.1.610756682.1721082489; _ga_PH6KHFG28N=GS1.1.1721162789.8.1.1721162916.14.0.0",
        "priority": "u=1, i",
        "referer": "https://www.webnovel.com/book/become-the-guard-ai-of-the-lost-civilization-after-transmigration_25215471605218605/administration-matrix_68177720919515612",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    json_text = json.loads(response.text)
    chapterInfo = json_text['data']['chapterInfo']
    return chapterInfo


if __name__ == "__main__":
    bookListdf = pd.read_csv('data/bookList.csv',dtype={'webnovelBookId':'string'})
    bookListdf = bookListdf.dropna(subset=['webnovelUrl'])
    bookList = bookListdf['webnovelBookId']
    collectedIds = [x.split('.')[0] for x in os.listdir('data/webnovelFreeChapterDates/')]#selectedd dates folder because I last save the dates
    print('Number of Collected Books:',len(collectedIds))
    missingIds = [x for x in bookList if x not in collectedIds]
    for bookId in missingIds:
        print(bookId)
        print('_________________')
        dfChapter = pd.read_csv('data/webnovelFreeChapterIds/' + bookId + '.csv',dtype={'chapterId':'string'})
        chapterIds = dfChapter['chapterId']
        dfContent = pd.DataFrame()
        timeBucket = []
        for chapterId in tqdm(chapterIds):
            chapterInfo = get_Content(bookId,chapterId)
            updateTime = chapterInfo['updateTime']
            publishTime = chapterInfo['publishTime']
            timeBucket.append([chapterId,publishTime,updateTime])
            contents = chapterInfo['contents']
            tempContent = pd.DataFrame(contents)
            tempContent['chapterId'] = chapterId
            dfContent = pd.concat([dfContent,tempContent],ignore_index=True)
        dfContent.to_csv('data/webnovelFreeChapterContent/' + bookId + '.csv',index=False)
        dfTime = pd.DataFrame(timeBucket,columns=['chapterId','publishTime','updateTime'])
        dfTime['publishTime'] = pd.to_datetime(dfTime['publishTime'],unit='ms')
        dfTime['updateTime'] = pd.to_datetime(dfTime['updateTime'],unit='ms')      
        dfTime.to_csv('data/webnovelFreeChapterDates/' + bookId + '.csv')

