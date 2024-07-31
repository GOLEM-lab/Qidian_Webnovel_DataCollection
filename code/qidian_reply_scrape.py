# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import time
import shutil
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from requests.exceptions import ConnectionError

# find comments with replies

def get_Replies(reviewId):
  urlReplies = "https://www.qidian.com/ajax/chapterReview/quoteReviewList"
  page = "1"
  page_int = 1
  replies = []
  while True:
    querystring = {"reviewId":reviewId,"page":page,"pageSize":"20","_csrfToken":"07cc5d3d-fb2b-4d08-8915-561aae1b4d86","w_tsfp":"ltvgWVEE2utBvS0Q6KzqnEymFjk7Z2R7xFw0D+M9Os09BqQiW5uE2IF5udfldCyCt5Mxutrd9MVxYnGHUdUseBMURsmYb5tH1VPHx8NlntdKRQJtA5LbDQMZK+4h6TZDdTkMLBbmjWwvJIETxORl3lwJ5SAm37ZlCa8hbMFbxl0yufqB0Jtsez6fxRXUEnT7J2MGf/jJ9p0x6PMUol2JowKuayctQP5X0zPQgG5GWz9atQS4AOhbNBWsJ86sWuQ2qTX6yjj2aIWu31ZytgUis2o8F9fymWSdehUdal5+Ziyxl7wiFP3odLBB5mpMArlMPVkS+lwc4eFt5BIdD3qgZCGPDedyvAEFW/df/pz9LCqX0s7kJhpF+ox8ywR15sNZ/TJgZ2n3Ld5aSGHLZXMPeY0Aa5y7NCoyUUNTXTdM5hUWPHhKF/lwMdLNsFTzdlFUwLJiMO+/euELaXiXBae2BrMyDmK088NjsBRfW6OoENYCb4k="}

    payload = ""
    headers = {
        "cookie": "supportWebp=true; newstatisticUUID=1716733315_1086707840; fu=1242577821",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
        "Connection": "keep-alive",
        "Cookie": "supportWebp=true; _gid=GA1.2.1050708547.1716387806; supportwebp=true; Hm_lvt_f00f67093ce2f38f215010b699629083=1716387812,1716537935; _yep_uuid=aa73416d-c47a-e71f-b966-c9f20dcd42d3; _csrfToken=07cc5d3d-fb2b-4d08-8915-561aae1b4d86; qdrsnew=7%7C3%7C0%7C0%7C1; traffic_utm_referer=; trkf=1; newstatisticUUID=1716733315_1086707840; fu=1597427940; Hm_lpvt_f00f67093ce2f38f215010b699629083=1716739294; _ga_FZMMH98S83=GS1.1.1716736383.17.1.1716739293.0.0.0; _ga=GA1.1.206926275.1716387806; _ga_PFYW0QLV3P=GS1.1.1716736383.17.1.1716739293.0.0.0; w_tsfp=ltvgWVEE2utBvS0Q6KzqnEymFjk7Z2R7xFw0D+M9Os09BqQiW5uE2IF5udfldCyCt5Mxutrd9MVxYnGHUdUseBMURsiWb5tH1VPHx8NlntdKRQJtA5LbDQMZK+4h6TZDdTkMLBbmjWwvJIETxORl3lwJ5SAm37ZlCa8hbMFbxl0yufqB0Jtsez6fxRXUEnT7J2MGf/jJ9p0x6PMUol2JowKuayctQP5X0zPQgG5GWz9atQS4AOhbNBWsJ86sWuQ2qTX6yjj2aIWu31ZytgUis2o8F9fymWSdehUdal5+Ziyxl7wiFP3odLBB5mpMArlMPVkS+lwc4eFt5BIdD3qgZCGPDedyvAEFW/df/pz9LCqX0s7kJhpF+ox8ywR15sNZ/TJgZ2n3Ld5aSGHLZXMPeY0Aa5y7NCoyUUNTXTdM5hUWPHhKF/lwMdLNsFTzdlFUwOU1Nu/tfOwMbX3EU6S6AOQ0Djnu+Ztlsx0LDfOqEtUFb4k=",
        "Referer": "https://www.qidian.com/chapter/1003692682/341658919/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    response = requests.request("GET", urlReplies, data=payload, headers=headers, params=querystring)
    replies_dict = json.loads(response.text)
    if len(replies_dict['data']['list']) > 0:
        replies += replies_dict['data']['list']
        page_int += 1
        page = str(page_int)
    else:
      break
  return replies



def join_replies(bookId):
    csv_files = os.listdir("data/qidianRepliesByComment/" + bookId)
    df = pd.DataFrame()
    for csv_file in csv_files:
        try:
          temp_df = pd.read_csv("data/qidianRepliesByComment/" + bookId + '/' + csv_file)
          df = pd.concat([df,temp_df],ignore_index=True)
        except pd.errors.EmptyDataError:
          pass
    df = df.drop_duplicates(subset=['reviewId'])
    df = df.reset_index(drop=True)
    df.to_csv("data/qidianReplies/" + bookId + '.csv',index=False)


if __name__ == "__main__":
  bookId = sys.argv[1]
  print(bookId)
  print('---------------')
  comments_df = pd.read_csv('data/qidianReviews/' + bookId + '.csv',dtype={'rootReviewId':'string'})
  commentIdsWithReplies = comments_df[comments_df['rootReviewReplyCount']!=0]
  reviewIds = commentIdsWithReplies['reviewId'].values.tolist()
  print('Number of Comments with Replies', len(reviewIds))
  collectedSegmentIds = [id.replace('.csv','') for id in os.listdir("data/qidianRepliesByComment/" + bookId)]#ids are string
  missingCommentIdsWithReplies = [str(id) for id in reviewIds if str(id) not in collectedSegmentIds]
  print('Number of Missing Comment Replies',len(missingCommentIdsWithReplies))
  for commentId in missingCommentIdsWithReplies:
      commentId = str(commentId)
      print('\t', commentId)
      try:
          replies = []
          replies += get_Replies(commentId)
          replies_df = pd.DataFrame(replies)
          replies_df.to_csv("data/qidianRepliesByComment/" + bookId + '/' + commentId + '.csv',index=False)
          #time.sleep(10*np.random.random())
      except (ConnectionError,ValueError):
          print('\t Connection Error Value. Waiting for a while!!')
          time.sleep(100) #sleep 100 seconds
      except KeyError:
          print('\t Key Error. Moving to the next one')
  #commnents with all repkies collected are  are joined and moved to the qidianReplies folder
  #repliesbycomment folder of that comment is deleted!
  if len(os.listdir("data/qidianRepliesByComment/" + bookId)) == len(commentIdsWithReplies):
    join_replies(bookId)
    shutil.rmtree("data/qidianRepliesByComment/" + bookId, ignore_errors=False)
  else:
     pass



   #comments_df = pd.read_csv('data/qidianReviewsByBook/' + bookId + '.csv',dtype={'rootReviewId':str})
   #commentIdsWithReplies = comments_df['rootReviewId'].loc[comments_df['rootReviewReplyCount']!=0]
   #print('Number of Comments with Replies', len(commentIdsWithReplies))
   #collectedSegmentIds = [id.replace('.csv','') for id in os.listdir("data/qidianRepliesByComment/" + bookId)]#ids are string
   #missingCommentIdsWithReplies = [id for id in commentIdsWithReplies if id not in collectedSegmentIds]#ids are string
   #print('Number of Missing Comment Replies',len(missingCommentIdsWithReplies))
   #for id in missingCommentIdsWithReplies:
   # commentId = str(id) #not needed but ...
   # print('\t', commentId)
   # try:
   #   replies = []
   #   replies += get_Replies(commentId)
   #   replies_df = pd.DataFrame(replies)
   #   replies_df.to_csv("data/qidianRepliesByComment/" + bookId + '/' + commentId + '.csv',index=False)
   #   #time.sleep(10*np.random.random())
   # except (ConnectionError,ValueError):
   #   print('\t Connection Error Value. Waiting for a while!!')
   #   time.sleep(100) #sleep 100 seconds
   # except KeyError:
   #   print('\t Key Error. Moving to the next one')
   #   f.write(str(id) + '\n')
   #if len(os.listdir("data/qidianRepliesByComment/" + bookId)) == len(commentIdsWithReplies):
   # join_replies(bookId)
   # shutil.rmtree("data/qidianRepliesByComment/" + bookId, ignore_errors=False)
   #else:
   # pass
