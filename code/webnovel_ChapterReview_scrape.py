import os
import sys
import time
import json
import requests
import pandas as pd
from tqdm import tqdm

def get_ChapterReviews(bookId,chapterId,lastReviewId,pageIndex):
    '''all parametrs are strings. pageIndex start from 1 and lastreviewId start from 0.'''
    url = "https://www.webnovel.com/go/pcm/chapterReview/getReviewList"

    querystring = {"_csrfToken":"4dbce8fb-ea3d-49d8-936a-b82dac7812cf","bookId":bookId,"chapterId":chapterId,"lastReviewId":lastReviewId,"orderType":"1","pageIndex":pageIndex,"_":"1722424601841"}

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
        "http": "http://00e9b91597e64c649fe3b4e345728af9:@api.zyte.com:8011/",
        "https": "http://00e9b91597e64c649fe3b4e345728af9:@api.zyte.com:8011/",
    }

    #response = requests.request("GET", url, data=payload, headers=headers, params=querystring,proxies=proxies_zyte,verify='/usr/local/share/ca-certificates/zyte-ca.crt')
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    json_response = json.loads(response.text)
    isLast = str(json_response['data']['isLast'])
    json_ChapterReplies = json_response['data']['chapterReviewItems']
    if len(json_ChapterReplies) !=0:
        lastReviewId = str(json_ChapterReplies[-1]['reviewId'])
        replies_df = pd.DataFrame(json_ChapterReplies)
        replies_df['chapterId'] = chapterId
    else:
        replies_df = pd.DataFrame()
        lastReviewId = -1
    
    return replies_df,isLast,lastReviewId





if __name__ == '__main__':
    bookId = sys.argv[1]
    print(bookId)
    print('---------------')

    dfMeta = pd.read_csv('data/webnovelFreeChapterMeta/' + bookId + '.csv',dtype={'chapterId':'string'})
    chapterIds = dfMeta['chapterId'].unique()

    for chapterId in tqdm(chapterIds):
        lastReviewId = '0'
        pageIndex_int = 1
        pageIndex = str(pageIndex_int)
        isLast = '0'
        dfChapter = pd.DataFrame()
        while isLast =='0':
            print(pageIndex)
            time.sleep(1)
            dfTemp,isLast,lastReviewId = get_ChapterReviews(bookId,chapterId,lastReviewId,pageIndex)
            dfChapter = pd.concat([dfChapter,dfTemp],ignore_index=True)
            pageIndex_int +=1
            pageIndex = str(pageIndex_int)
            lastReviewId = str(lastReviewId)
        dfChapter.to_csv('data/webnovelReviews_Chapter_ByChapter/' + bookId + '/' + chapterId + '.csv',index=False)


