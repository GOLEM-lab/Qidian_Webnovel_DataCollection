import os
import sys
import json
import time
import requests
import numpy as np
import pandas as pd
from lxml import html
from tqdm import tqdm
from datetime import datetime
from bs4 import BeautifulSoup as bs





def get_ParagraphReplies(chapterId,paragraphId,reviewId,lastTime):
  replies_df = pd.DataFrame()
  url = "https://www.webnovel.com/go/pcm/paragraphReview/getReieweReplys"

  querystring = {"_csrfToken":"4dbce8fb-ea3d-49d8-936a-b82dac7812cf","chapterId":chapterId,"paragraphId":paragraphId,"reviewId":reviewId,"lastTime":lastTime,"_":"1721747176021"}

  payload = ""
  headers = {
      "accept": "application/json, text/javascript, */*; q=0.01",
      "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,th;q=0.6,tr;q=0.5,nl;q=0.4",
      "cookie": "_csrfToken=4dbce8fb-ea3d-49d8-936a-b82dac7812cf; webnovel_uuid=1721082484_17363682; webnovel-content-language=en; webnovel-language=en; para-comment-tip-show=1; bookCitysex=1; e1=%7B%22l1%22%3A%2299%22%7D; e2=%7B%22l1%22%3A%2299%22%7D; _gid=GA1.2.852697514.1721511577; Hm_lvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721373103,1721391429,1721511577,1721772622; HMACCOUNT=66714B21096099E3; AMP_TOKEN=%24NOT_FOUND; _gat=1; dontneedgoogleonetap=1; Hm_lpvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721772629; _ga_PH6KHFG28N=GS1.1.1721772622.35.1.1721772629.53.0.0; _ga=GA1.1.610756682.1721082489",
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
  json_replies = json_response['data']['paragraphReviewItems']
  
  replies_df = pd.DataFrame(json_replies)
  replies_df['chapterId'] = chapterId
  replies_df['paragraphId'] = paragraphId
  replies_df['sourceReviewId'] = reviewId

  isLast = str(json_response['data']['isLast'])
  lastTime = str(json_response['data']['lastTime'])
  return replies_df,isLast,lastTime



if __name__ == '__main__':
    bookId = sys.argv[1]
    print(bookId)
    print('---------------')
    time.sleep(2)
    reviews = pd.read_csv('data/webnovelReviews_Paragraph_ByBook/'+str(bookId)+'.csv',dtype={'chapterId':'str','paragraphId':'str','reviewId':'str'})
    reviewsWithReplies = reviews.loc[reviews['replyAmount']!=0]
    print(len(reviewsWithReplies))
    replies = pd.DataFrame()
    for i,row in tqdm(reviewsWithReplies.iterrows()):
        chapterId = row['chapterId']
        paragraphId = row['paragraphId']
        reviewId = str(row['reviewId'])
        while True:
            try:
                isLast = '0'
                lastTime = '0'
                while isLast == '0':
                    temp,isLast,lastTime = get_ParagraphReplies(chapterId,paragraphId,reviewId,lastTime)
                    replies = pd.concat([replies,temp],ignore_index=True)
                break
            except:
                print('JSON Error. Retrying!')
                continue

    replies.to_csv('data/webnovelReplies_Paragraph_ByBook/'+str(bookId)+'.csv',index=False)