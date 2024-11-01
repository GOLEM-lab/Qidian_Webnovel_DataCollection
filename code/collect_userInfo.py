import os
import re
import json
import time
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

# This function with the currect querystring and headers should work.
# But if you receive connection error, it may be because _csrfToken in querystring and/or cookie in the headers are expired.
# update them 
def get_UserInfo(userId):
    userId = str(userId)
    userUrl = 'https://my.qidian.com/user/' + userId
    header = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
'Content-Type': 'text/html; charset=utf-8',
'set-cookie':'csrfToken=yQltzgNj44UErVXluXQo0oDkcXXlzeJyBg1npj5F; expires=Fri, 06-Jun-2025 20:56:02 GMT; path=/; domain=.qidian.com',
'X-NWS-LOG-UUID': '5059556769341264456'}
    r = requests.get(userUrl,headers=header)
    soup = bs(r.text,features="html.parser")

    userInfo = soup.find_all('div',{'class':'header-msg'})[0]
    levelInfo = userInfo.find_all('h3',{'data-id':userId})[0].text
    genderInfo = userInfo.find_all('div',{'class':'header-msg-desc'})[0].text
    nameInfo = userInfo.find_all('div',{'class':'header-msg-title'})[0].text
    nameInfo = nameInfo.split(':')[-1].strip()
    numberOfFollowers = userInfo.find_all('span',{'class':"mr8"})[0].text[-1]
    if numberOfFollowers == '-':
        numberOfFollowers = np.nan
    else:
        numberOfFollowers = int(numberOfFollowers)
    numberOfFans = userInfo.find_all('span',{'class':"ml12 mr8"})[0].text[-1]
    if numberOfFans == '-':
        numberOfFans = np.nan
    else:
        numberOfFans = int(numberOfFans)
    return [userId,levelInfo,genderInfo,nameInfo,numberOfFollowers,numberOfFans]


# This function with the currect querystring and headers should work.
# But if you receive connection error, it may be because _csrfToken in querystring and/or cookie in the headers are expired.
# update them 
def get_UserHistory(userId):
    userId = str(userId)
    url = "https://my.qidian.com/ajax/User/FriendHistory"

    querystring = {"_csrfToken":"07cc5d3d-fb2b-4d08-8915-561aae1b4d86","id":userId}

    payload = ""
    headers = {
        "cookie": "supportWebp=true; newstatisticUUID=1716733315_1086707840; fu=1242577821; _csrfToken=yQltzgNj44UErVXluXQo0oDkcXXlzeJyBg1npj5F",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
        "Cookie": "supportWebp=true; supportwebp=true; _csrfToken=07cc5d3d-fb2b-4d08-8915-561aae1b4d86; qdrsnew=7%7C3%7C0%7C0%7C1; newstatisticUUID=1716733315_1086707840; fu=1597427940; traffic_search_engine=; _gid=GA1.2.592479407.1717706495; traffic_utm_referer=; se_ref=; Hm_lvt_f00f67093ce2f38f215010b699629083=1716387812,1716537935,1716983369,1717706496; _ga_FZMMH98S83=GS1.1.1717706494.30.1.1717706542.0.0.0; _ga=GA1.1.206926275.1716387806; _ga_PFYW0QLV3P=GS1.1.1717706494.30.1.1717706542.0.0.0; Hm_lpvt_f00f67093ce2f38f215010b699629083=1717706543",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    dictResponse = json.loads(response.text)
    footprintData = dictResponse['data']['historyData']

    return list(footprintData.values())

def main():
    df = pd.read_csv('data/userList.csv',dtype={'ids':'string'})
    userIds = df['ids'].unique()
    print(len(userIds))
    usersAll = []
    for userId in tqdm(userIds):
        try:
            userInfo = get_UserInfo(userId)
            userHistory = get_UserHistory(userId)
            userAll = userInfo + userHistory
            usersAll.append(userAll)
        except:
            print(userId)
            pass
    return usersAll


if __name__ == "__main__":
    usersAll = main()
    colnames = ['userId','levelInfo','genderInfo','nameInfo','numberOfFollowers','numberOfFans','bookshelfCollection','subscribedWorks',
                'rewardedWorks','monthlyVotes','recommendationVotes']
    df = pd.DataFrame(usersAll,columns=colnames)
    df.to_csv('data/qidianUserProfiles.csv',index=False)





