import os
import json
import time
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
'''collects the total number of chapter reviews and replies.generates a single file.'''

def get_ChapterReviewAmount(bookId,chapterId):
    url = "https://www.webnovel.com/go/pcm/chapterReview/getReviewList"

    querystring = {"_csrfToken":"4dbce8fb-ea3d-49d8-936a-b82dac7812cf","bookId":bookId,"chapterId":chapterId,"lastReviewId":"0","orderType":"1","pageIndex":"1","_":"1722424601841"}

    payload = ""
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,th;q=0.6,tr;q=0.5,nl;q=0.4",
        "cookie": "_csrfToken=4dbce8fb-ea3d-49d8-936a-b82dac7812cf; webnovel_uuid=1721082484_17363682; webnovel-content-language=en; webnovel-language=en; para-comment-tip-show=1; bookCitysex=1; e1=%7B%22l1%22%3A%2299%22%7D; e2=%7B%22l1%22%3A%2299%22%7D; _fsae=1721832606945; Hm_lvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721981014,1722025833,1722243779,1722424590; HMACCOUNT=66714B21096099E3; _gid=GA1.2.1001528267.1722424590; dontneedgoogleonetap=1; Hm_lpvt_5e0df2e5fd02494fa1d84eca4a8baea4=1722424603; _ga_PH6KHFG28N=GS1.1.1722424590.53.1.1722424605.45.0.0; _ga=GA1.1.610756682.1721082489",
        "priority": "u=1, i",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    proxies_zyte = {
        "http": "http://7719922b3293465392ccc096980842e2:@api.zyte.com:8011/",
        "https": "http://7719922b3293465392ccc096980842e2:@api.zyte.com:8011/",
    }

    #response = requests.request("GET", url, data=payload, headers=headers, params=querystring,proxies=proxies_zyte,verify='/usr/local/share/ca-certificates/zyte-ca.crt')
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    json_response = json.loads(response.text)
    return json_response['data']['baseInfo']['reviewAmount']
    
if __name__ == '__main__':
    with open('data/webnovelBookList.txt','r') as f:
        bookList = [x.strip() for x in f.readlines()]
    info = []
    for bookId in tqdm(bookList):
        dfMeta = pd.read_csv('data/webnovelFreeChapterMeta/' + bookId + '.csv',dtype={'chapterId':'string'})
        chapterIds = dfMeta['chapterId'].unique()
        for chapterId in chapterIds:
            amount = get_ChapterReviewAmount(bookId,chapterId)
            info.append([bookId,chapterId,amount])
    df = pd.DataFrame(info,columns=['bookId','chapterId','chapterReviewAmount'])
    df.to_csv('data/webnovel_ChapterReviewAmount.csv',index=False)