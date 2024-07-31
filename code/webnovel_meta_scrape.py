import os
import json
import time
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm



def get_ReviewNumber(chapterId):
    url = "https://www.webnovel.com/go/pcm/paragraphReview/getReiewNum"

    querystring = {"_csrfToken":"4dbce8fb-ea3d-49d8-936a-b82dac7812cf","chapterId":chapterId,"_":"1721157976019"}

    payload = ""
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,th;q=0.6,tr;q=0.5,nl;q=0.4",
        "cookie": "_csrfToken=4dbce8fb-ea3d-49d8-936a-b82dac7812cf; webnovel_uuid=1721082484_17363682; webnovel-content-language=en; webnovel-language=en; _gid=GA1.2.826710995.1721082489; dontneedgoogleonetap=1; para-comment-tip-show=1; Hm_lvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721082488,1721141260,1721156823; HMACCOUNT=66714B21096099E3; AMP_TOKEN=%24NOT_FOUND; Hm_lpvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721157938; _gat=1; _ga=GA1.1.610756682.1721082489; _ga_PH6KHFG28N=GS1.1.1721156823.7.1.1721157975.21.0.0",
        "priority": "u=1, i",
        "referer": "https://www.webnovel.com/book/full-marks-hidden-marriage-pick-up-a-son-get-a-free-husband_8060642606003005/seven-months-pregnant_21657035804306187",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }



    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    json_text = json.loads(response.text)
    df = pd.DataFrame(json_text['data']['paragraphItems'])
    return df



if __name__ == "__main__":
    bookListdf = pd.read_csv('data/bookList.csv',dtype={'webnovelBookId':'string'})
    bookListdf = bookListdf.dropna(subset=['webnovelUrl'])
    bookList = bookListdf['webnovelBookId']
    collectedIds = [x.split('.')[0] for x in os.listdir('data/webnovelFreeChapterMeta/')]
    print('Number of Collected Books:',len(collectedIds))
    missingIds = [x for x in bookList if x not in collectedIds]
    for bookId in missingIds:
        print(bookId)
        dfChapter = pd.read_csv('data/webnovelFreeChapterIds/' + bookId + '.csv',dtype={'chapterId':'string'})
        chapterIds = dfChapter['chapterId']
        df = pd.DataFrame()
        print(len(chapterIds))
        for chapterId in tqdm(chapterIds):
            temp = get_ReviewNumber(chapterId)
            temp['chapterId'] = chapterId
            temp['bookId'] = bookId
            df = pd.concat([df,temp],ignore_index=True)
        df.to_csv('data/webnovelFreeChapterMeta/' + bookId + '.csv',index=False)



