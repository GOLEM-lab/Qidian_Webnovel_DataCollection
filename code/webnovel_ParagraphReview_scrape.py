import os
import sys
import time
import json
import requests
import pandas as pd
from tqdm import tqdm


def get_ParagraphReviews(chapterId,paragraphId,lastTime):
    url = "https://www.webnovel.com/go/pcm/paragraphReview/getReiewList"

    querystring = {"_csrfToken":"4dbce8fb-ea3d-49d8-936a-b82dac7812cf","chapterId":chapterId,"paragraphId":paragraphId,"lastTime":"0","_":"1721834832157"}

    payload = ""
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,th;q=0.6,tr;q=0.5,nl;q=0.4",
        "cookie": "_csrfToken=4dbce8fb-ea3d-49d8-936a-b82dac7812cf; webnovel_uuid=1721082484_17363682; webnovel-content-language=en; webnovel-language=en; para-comment-tip-show=1; bookCitysex=1; e1=%7B%22l1%22%3A%2299%22%7D; e2=%7B%22l1%22%3A%2299%22%7D; _gid=GA1.2.852697514.1721511577; dontneedgoogleonetap=1; Hm_lvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721391429,1721511577,1721772622,1721831950; HMACCOUNT=66714B21096099E3; AMP_TOKEN=%24NOT_FOUND; _fsae=1721832606945; Hm_lpvt_5e0df2e5fd02494fa1d84eca4a8baea4=1721834833; _gat=1; _ga_PH6KHFG28N=GS1.1.1721831951.39.1.1721834833.24.0.0; _ga=GA1.1.610756682.1721082489",
        "priority": "u=1, i",
        "referer": "https://www.webnovel.com/book/seeking-the-flying-sword-path_8591840605001105/return_23063639992885692",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    proxies_zyte = {
        "http": "http://7719922b3293465392ccc096980842e2:@api.zyte.com:8011/",
        "https": "http://7719922b3293465392ccc096980842e2:@api.zyte.com:8011/",
    }
    
    #response = requests.request("GET", url, data=payload, headers=headers, params=querystring,proxies=proxies_zyte,verify='/usr/local/share/ca-certificates/zyte-ca.crt' )
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    
    json_response = json.loads(response.text)
    dfReviews = pd.DataFrame()
    dfReviews = pd.concat([dfReviews,pd.DataFrame(json_response['data']['topParagraphTopicItems'])],ignore_index=True)
    dfReviews = pd.concat([dfReviews,pd.DataFrame(json_response['data']['paragraphTopicItems'])],ignore_index=True)
    
    isLast = str(json_response['data']['isLast'])
    lastTime = str(json_response['data']['lastTime'])

    return dfReviews,isLast,lastTime

if __name__ == '__main__':
    bookId = sys.argv[1]
    print(bookId)
    print('---------------')

    
    dfMeta = pd.read_csv('data/webnovelFreeChapterMeta/' + bookId + '.csv',dtype={'chapterId':'string'})
    
    #groupby chapterId and  count the reviewAmount
    meta = pd.read_csv('data/webnovelFreeChapterMeta/' + bookId + '.csv', dtype={'chapterId':'string'})
    meta = dfMeta[['paragraphId','reviewAmount']][dfMeta['reviewAmount']!=0]

    chapterIds = dfMeta['chapterId'].unique()
    collectedChapterIds = [x.split('.')[0] for x in os.listdir('data/webnovelReviews_Paragraph_ByChapter/' + bookId + '/')]
    print('Number of Collected Ids',len(collectedChapterIds))
    missingChapterIds = [x for x in chapterIds if x not in collectedChapterIds]
    print('Number of Missing Chapters',len(missingChapterIds))
    
    if len(missingChapterIds) !=0:
        for chapterId in tqdm(missingChapterIds):
            print('Chapter',chapterId)
            dfTempChapter = pd.DataFrame()
            paragraphIds = dfMeta['paragraphId'][dfMeta['chapterId'] == chapterId]
            os.makedirs('data/webnovelReviews_Paragraph_ByParagraph/' + bookId + '/' + chapterId,exist_ok=True)
            collectedParagraphIds = [x.split('.')[0] for x in os.listdir('data/webnovelReviews_Paragraph_ByParagraph/' + bookId + '/' + chapterId + '/')]
            missingParagraphIds = [x for x in paragraphIds if x not in collectedParagraphIds]
            print('Number of Missing Paragraphs',len(missingParagraphIds))
            if len(missingParagraphIds) != 0:
                for paragraphId in tqdm(missingParagraphIds):
                    try:
                        lastTime = '0'
                        isLast = '0'
                        while isLast == '0':
                            df,isLast,lastTime = get_ParagraphReviews(chapterId,paragraphId,lastTime)
                            df['chapterId'] = chapterId
                            df['paragraphId'] = paragraphId
                            dfTempChapter = pd.concat([dfTempChapter,df],ignore_index=True)
                            isLast = str(isLast)
                            lastTime = str(lastTime)
                        #save the paragraph
                        dfTempChapter.to_csv('data/webnovelReviews_Paragraph_ByParagraph/' + bookId + '/' + chapterId + '/' + paragraphId + '.csv',index=False)
                    except:
                        print('JSONDecodeError')
                        break
            else:
                print('\t chapter is complete')        
    else:
        print('book is complete')
        print('\n')