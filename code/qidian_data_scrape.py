# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import time
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from requests.exceptions import ConnectionError


def get_chapterCommentSummary(bookId,chapterId,referer):
  urlSummary = "https://www.qidian.com/ajax/chapterReview/reviewSummary"
  querystring = {"bookId":bookId,"chapterId":chapterId,"_csrfToken":"07cc5d3d-fb2b-4d08-8915-561aae1b4d86","w_tsfp":"ltvgWVEE2utBvS0Q6KzqnEymFjk7Z2R7xFw0D+M9Os09BqQiWpqF1YR+uNfldCyCt5Mxutrd9MVxYnGHUdUteREQQM6Vb5tH1VPHx8NlntdKRQJtA5LbDQMZK+4h6TZDdTkMLBbmjWwvJIETxORl3lwJ5SAm37ZlCa8hbMFbxl0yufqB0Jtsez6fxRXUEnT7J2MGf/jJ9p0y+OoJoni/oAamfRk9Frk0ghrNjlFLG3tX4BG7d+9UNxqlIdutXr5o/HO3l3uOPoWvrRUn4FYyuBc8C8D231qZbDQSRFQwMAangcokfP34M7Im7SxPDq4dVF1BqQcEves4/FlKCynsMSCOV/4uvQYSWuAIrZPzO3aUiojmMghZ6N0ulVs3u5IF7zhyZ2n3Ld5aSGHLZXMPeY0Aa5y7JjYgAhsGDmwPo0gENmpZXugibI6X7xC1KEpc1eMxbeTqf+AEaCjFAaLuDeA8CCPx"}

  payload = ""
  headers = {
      "cookie": "supportWebp=true; newstatisticUUID=1716733315_1086707840; fu=1242577821",
      "Accept": "application/json, text/plain, */*",
      "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
      "Cookie": "supportWebp=true; _gid=GA1.2.1050708547.1716387806; supportwebp=true; Hm_lvt_f00f67093ce2f38f215010b699629083=1716387812,1716537935; _yep_uuid=aa73416d-c47a-e71f-b966-c9f20dcd42d3; _csrfToken=07cc5d3d-fb2b-4d08-8915-561aae1b4d86; qdrsnew=7%7C3%7C0%7C0%7C1; traffic_utm_referer=; trkf=1; newstatisticUUID=1716733315_1086707840; fu=1597427940; Hm_lpvt_f00f67093ce2f38f215010b699629083=1716737546; _gat_gtag_UA_199934072_2=1; _ga_PFYW0QLV3P=GS1.1.1716736383.17.1.1716738404.0.0.0; _ga=GA1.1.206926275.1716387806; _ga_FZMMH98S83=GS1.1.1716736383.17.1.1716738404.0.0.0; w_tsfp=ltvgWVEE2utBvS0Q6KzqnEymFjk7Z2R7xFw0D+M9Os09BqQiWpqF1YR+uNfldCyCt5Mxutrd9MVxYnGHUdUteREQQM2Tb5tH1VPHx8NlntdKRQJtA5LbDQMZK+4h6TZDdTkMLBbmjWwvJIETxORl3lwJ5SAm37ZlCa8hbMFbxl0yufqB0Jtsez6fxRXUEnT7J2MGf/jJ9p0y+OoJoni/oAamfRk9Frk0ghrNjlFLG3tX4BG7d+9UNxqlIdutXr5o/HO3l3uOPoWvrRUn4FYyuBc8C8D231qZbDQSRFQwMAangcokfP34M7Im7SxPDq4dVF1BqQcEves4/FlKCynsMSCOV/4uvQYSWuAIrZPzO3aUiojmMghZ6N0ulVs3u5IF7zhyZ2n3Ld5aSGHLZXMPeY0Aa5y7JjYgAhsGDmwPo0gENmpeC74qPNGcuBW3fUYKhLM7Y7HvLOwLbnnFA/fpDbNjCCPx",
      "Referer": referer,
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
  }

  response = requests.request("GET", urlSummary, data=payload, headers=headers, params=querystring)

  commentSummary = json.loads(response.text)
  commentSummary = pd.DataFrame(commentSummary['data']['list'])
  return commentSummary

#Comments
def get_segmentComments(bookId,chapterId,segmentId,referer):
  urlComments = "https://www.qidian.com/ajax/chapterReview/reviewList"
  page = "1"
  page_int = 1
  comments = []
  while True:
    querystring = {"bookId":bookId,"chapterId":chapterId,"page":page,"pageSize":"20","segmentId":segmentId,"type":"2","_csrfToken":"07cc5d3d-fb2b-4d08-8915-561aae1b4d86","w_tsfp":"ltvgWVEE2utBvS0Q6KzqnEymFjk7Z2R7xFw0D+M9Os09BqQiW52F2YF5t9fldCyCt5Mxutrd9MVxYnGHUdUsfhEdRsWZb5tH1VPHx8NlntdKRQJtA5LbDQMZK+4h6TZDdTkMLBbmjWwvJIETxORl3lwJ5SAm37ZlCa8hbMFbxl0yufqB0Jtsez6fxRXUEnT7J2MGf/jJ9p0y+OoJonigvBi/OVgCUeUdizzGwCtrD3gj4heydu9VNwmvJZ33Ca10+HGKliz0HpOo2BAm6Vk2uQs/BJWljmDfLAJFNQltJQnl1919Mfu+NZInuSQbWu8aHgRA90tg4fc6jUFaDy75KTXaEPkOtxUCQJ0KvI/6HXSeg8T5I3xZ7459kA80749TvTogem2jLdZHQGjKYG4Kf4xROsm6Zi5mWUVBQSUdtEtJfiUJV/kpe4ee6xe2K0Ne0rEzZOftKeQMaX3EUPa/BbY1XDG8+5Jm9wkYWa/7QolAOJkRCjeKhpusxNAhcoW221rmEXvStOxZKmLlAvBxe830x/kjvBDa"}
    payload = ""

    headers = {
        "cookie": "supportWebp=true; newstatisticUUID=1716733315_1086707840; fu=1242577821",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
        "Cookie": "supportWebp=true; _gid=GA1.2.1050708547.1716387806; supportwebp=true; Hm_lvt_f00f67093ce2f38f215010b699629083=1716387812,1716537935; _yep_uuid=aa73416d-c47a-e71f-b966-c9f20dcd42d3; _csrfToken=07cc5d3d-fb2b-4d08-8915-561aae1b4d86; qdrsnew=7%7C3%7C0%7C0%7C1; traffic_utm_referer=; trkf=1; newstatisticUUID=1716733315_1086707840; fu=1597427940; Hm_lpvt_f00f67093ce2f38f215010b699629083=1716739294; _ga_FZMMH98S83=GS1.1.1716736383.17.1.1716739293.0.0.0; _gat_gtag_UA_199934072_2=1; _ga=GA1.1.206926275.1716387806; _ga_PFYW0QLV3P=GS1.1.1716736383.17.1.1716739293.0.0.0; w_tsfp=ltvgWVEE2utBvS0Q6KzqnEymFjk7Z2R7xFw0D+M9Os09BqQiW52F2YF5t9fldCyCt5Mxutrd9MVxYnGHUdUsfhEdRsSWb5tH1VPHx8NlntdKRQJtA5LbDQMZK+4h6TZDdTkMLBbmjWwvJIETxORl3lwJ5SAm37ZlCa8hbMFbxl0yufqB0Jtsez6fxRXUEnT7J2MGf/jJ9p0y+OoJonigvBi/OVgCUeUdizzGwCtrD3gj4heydu9VNwmvJZ33Ca10+HGKliz0HpOo2BAm6Vk2uQs/BJWljmDfLAJFNQltJQnl1919Mfu+NZInuSQbWu8aHgRA90tg4fc6jUFaDy75KTXaEPkOtxUCQJ0KvI/6HXSeg8T5I3xZ7459kA80749TvTogem2jLdZHQGjKYG4Kf4xROsm6Zi5mWUVBQSUdtEtJfiUJV/kpe4ee6xe2K0Ne0rEzZOftKeQMaX3EUPa/BbY1XDG8+5Jm9wkYWa/7QolAOJkRCjeK25KtwYwncIayjg/gESqH5+0PITC/VvggLp+llPktuRDa",
        "Referer": referer,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    response = requests.request("GET", urlComments, data=payload, headers=headers, params=querystring)
    #time.sleep(10*np.random.random())
    comments_dict = json.loads(response.text)
    if len(comments_dict['data']['list']) > 0:
      comments += comments_dict['data']['list']
      page_int += 1
      page = str(page_int)
    else:
      break
  return comments

def get_Comments(bookId,chapterIds):
  print('Total number of chapters', len(chapterIds))
  referers = ['wwww.google.com','www.qidian.com','www.bing.com','www.duckduckgo.com','www.baidu.com']
  noComment = []
  for chapterId in chapterIds:
    try:
      print('Chapter ',chapterId)
      i = np.random.randint(0,5)
      referer = referers[i]
      commentSummary = get_chapterCommentSummary(bookId,chapterId,referer)
      print('Number of segments in this chapter:',len(commentSummary))
      chComments = []
      if commentSummary.shape[0] != 0:
        for segmentId in commentSummary['segmentId']:
          segmentId = str(segmentId)
          segmentComments = get_segmentComments(bookId,chapterId,segmentId,referer)
          chComments += segmentComments
          #time.sleep(50*np.random.random())
        comments_df = pd.DataFrame(chComments)
        print('Saving file',chapterId)
        comments_df.to_csv('data/qidianReviews/' + bookId + '/' + chapterId + '.csv',index=False)
        time.sleep(10*np.random.random())
      else:
        noComment.append(chapterId)
    except ConnectionError:
      print('Connection Error. Saving what has been collected sofar and Waiting for a while!!')
      comments_df.to_csv('data/qidianReviews_incomplete/' + bookId + '/' + chapterId + '.csv',index=False)
      time.sleep(300) #sleep 5 minutes
  with open('data/qidianNoCommentChapterIds/' + bookId + '.txt','a') as f:
    for id in noComment:
      f.writelines(id + '\n')


if __name__ == "__main__":
  
  bookId = sys.argv[1]
  print(bookId)
  print('---------------')
  with open('data/qidianFreeChapterIds/' + bookId + '.txt', 'r') as f:
    chapterIds = [b.strip() for b in f.readlines()]
  fileList = os.listdir('data/qidianReviews/' + bookId)
  collectedIds = [file.split('.')[0] for file in fileList]
  missingIds = [id for id in chapterIds if id not in collectedIds]
  #chapterIds = ['413043721', '413046082', '413046889', '414056259', '414115182', '414145253', '414262319', '414262459', '414608351', '414638975', '414797898', '414858894', '414883901', '415024650', '415194462', '415279173', '415307714', '415383820', '415408941', '415476253', '415504312', '415504752', '415574607', '415663057', '415666269', '415771109', '415771296', '415771449', '415928643', '415928819', '416043076', '416043325', '416116050', '416116251', '416204803', '416204882', '416295707', '416296482', '416412185', '416486846', '416512818', '416574679', '416620074', '416690926', '416692941', '416777099', '416777222', '416868023', '416885978', '416886205', '417012721', '417012793', '417122580', '417122813', '417236153', '417236281', '417318587', '417318821', '417428499', '417516699', '417540809', '417540978', '417640691', '417716071', '417737588', '417737897', '417858623', '417942762', '417989667', '418113046', '418185071', '418305952', '418332486', '418397318', '418419873', '418496765', '418587646', '418700240', '418732673', '418732947', '418862780', '418939292', '418987857', '419074516', '419160451', '419242513', '419242838', '419338230', '419346306', '419346402', '419494715', '419581202', '419622717', '419622955', '419808435', '419893409', '419930462', '419930564', '420042802', '420114484', '420143063', '420143191', '420233617', '420233983', '420329615', '420329763', '420465009', '420466743', '420574341', '420574863', '420680586', '420680666', '420831489', '420831910', '420959597', '420960367', '421077630', '421078072', '421217166', '421217463', '421314774', '421317646']
  get_Comments(bookId,missingIds)
  


