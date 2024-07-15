import os
import re
import json
import time
import requests
import numpy as np
import pandas as pd
#from lxml import html
from tqdm import tqdm
from bs4 import BeautifulSoup as bs



def get_QidianMeta(url,bookId):
  payload = ""
  headers = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
      "Cookie": "_yep_uuid=02c2c6fd-521e-a2cd-6ac9-4f70e60b34aa; x-waf-captcha-referer=; newstatisticUUID=1713391240_558590204; _csrfToken=ynkbISkpAKNw2fcRba2COBIpyFXHMBCNiZYqBhfq; fu=310525340; _ga_FZMMH98S83=GS1.1.1713391243.1.0.1713391243.0.0.0; _gid=GA1.2.950724054.1713391244; _gat_gtag_UA_199934072_2=1; _ga_PFYW0QLV3P=GS1.1.1713391244.1.0.1713391244.0.0.0; _ga=GA1.1.1339574039.1713391244; traffic_utm_referer=; Hm_lvt_f00f67093ce2f38f215010b699629083=1713391245; Hm_lpvt_f00f67093ce2f38f215010b699629083=1713391245; w_tsfp=ltvgWVEE2utBvS0Q6KnqnUqsFTE7Z2R7xFw0D+M9Os09A6AoU5yB2Yd9u9fldCyCt5Mxutrd9MVxYnGCVd8kfxQcQMuVb5tH1VPHx8NlntdKRQJtA82OC18fJLsj7DRBKD9WLUOwjz4vI9VFyLNi2A8L5yon37ZlCa8hbMFbixsAqOPFm/97DxvSliPXAHGHM3wLc+6C6rgv8LlSgW2DugDuLi11A7pB1kyQ0yAdG3pV8w2pJbsDal7wcpK9Uv8wrTPzwjn3apCs2RYj4VA3sB49AtX02TXKL3ZEIAtrZUqukO18Lv3wdaN4qzsLCf4eS11Eql4QtrY++BJKCCu8ZSHbAPx7s1ECQ/Jb98m+NA=="
  }
  response = requests.request("GET", url, data=payload, headers=headers)
  soup = bs(response.text,'html')
  book_meta = {'bookId':bookId}

  qidian_meta = soup.find_all('meta')

  for meta in qidian_meta:
    if meta.get('property') in ['og:description','og:title','og:novel:category','og:novel:author','og:novel:author_link',
                                'og:novel:update_time','og:novel:latest_chapter_name','og:novel:latest_chapter_url']:
      book_meta.update({meta.get('property'):meta.get('content')})
    if meta.get('name') in ['keywords','']:
      book_meta.update({meta.get('name'):meta.get('content')})
    if meta.get('name') == 'description':
      book_meta.update({'numberOfChapters':re.search('[0-9]+',meta.get('content')).group()})

  genre = soup.find_all('a',{'data-eid':'qd_G10'})[0].get('title')
  book_meta.update({'genre':genre[:-2]})
  numberOfWords, totalRecommendations,numberOfWeeksRecommended = soup.find_all('p',{'class':'count'})[0].text.split(' ')
  book_meta.update({'numberOfWords':numberOfWords[:-1], 'totalRecommendations':totalRecommendations[:-3],'numberOfWeeksRecommended':numberOfWeeksRecommended[:-2]})
  return book_meta



if __name__ == "__main__":
    allMeta = []
    errors = []
    numberOfFreeChapters = []
    bookList = pd.read_csv("data/bookList.csv")
    bookList = bookList.dropna()
    for i,row in tqdm(bookList.iterrows()):
        url = row['qidianUrl']
        bookId = str(int(row['qidianBookId']))
        try:
            bookMeta = get_QidianMeta(url,bookId)
            with open('data/qidianFreeChapterIds/' + bookId + '.txt',) as f:
                chapterIds = [b.strip() for b in f.readlines()]
            bookMeta.update({'numberOfFreeChapters':len(chapterIds)})
            allMeta.append(bookMeta)
        except:
            errors.append(url)
        time.sleep(10)
    qidianMeta = pd.DataFrame(allMeta)
    new_column_order = ['bookId', 'keywords', 'numberOfChapters', 'numberOfFreeChapters','og:title', 'og:description',
       'og:novel:category', 'og:novel:author', 'og:novel:author_link',
       'og:novel:update_time', 'og:novel:latest_chapter_name',
       'og:novel:latest_chapter_url', 'genre', 'numberOfWords',
       'totalRecommendations', 'numberOfWeeksRecommended']
    qidianMeta = qidianMeta[new_column_order] 
    qidianMeta.to_csv('data/qidianMeta_' +str(pd.Timestamp.today()) + '.csv',index=False)


