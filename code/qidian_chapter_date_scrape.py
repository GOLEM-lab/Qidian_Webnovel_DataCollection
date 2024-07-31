import sys
import json
import requests
import pandas as pd



def get_ChapterDates(bookId):
    url = "https://www.qidian.com/ajax/book/category"

    querystring = {"_csrfToken":"JcOUNoZ4zXfv7GcbCNxfNq0CHxqRLZXqgT9bUjMR","bookId":bookId,"w_tsfp":"ltvgWVEE2utBvS0Q6KjvnUqnHjg7Z2R7xFw0D+M9Os0+AaIgVZ6G1YZ9uNfldCyCt5Mxutrd9MVxYnKAV9cifRIRQM2Tb5tH1VPHx8NlntdKRQJtA5zbWlZLde1w7mNFLz5cd0Cwjzx/JIdBn7IxjF1Z4SZ337ZlCa8hbMFbxl0yufqB0Jtsez+Yyw6FRUDKI2EKfeCevf5z28MDtH2KgQSgeQVhAM44gzr3q3d1CjJLt1e8A7oPRmLldbDuWJ5I5XKRvlOfK8fI0ERGuy1VpRw7UIqrgkyeOnUwIQtrZl67gLgseby3JLd3525bAf0TW1MHqQ8ZteI5+URPDSi9YHWPBfp6tQAARvJZ/82seSvF1pr+PBoKsIh9zhhy5oAP/Tsjb2DyL4hdTTefbHVdKosJbpW+Mi46BEdUCz5Nt0MRLjU="}

    payload = ""
    headers = {
        "cookie": "supportWebp=true; newstatisticUUID=1716733315_1086707840; fu=1242577821; _csrfToken=yQltzgNj44UErVXluXQo0oDkcXXlzeJyBg1npj5F",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,th;q=0.6,tr;q=0.5,nl;q=0.4",
        "Connection": "keep-alive",
        "Cookie": "newstatisticUUID=1718809397_52477868; fu=1798162881; e2=; e1=%7B%22l6%22%3A%22%22%2C%22l1%22%3A%22%22%2C%22pid%22%3A%22qd_p_qidian%22%2C%22eid%22%3A%22%22%7D; _csrfToken=JcOUNoZ4zXfv7GcbCNxfNq0CHxqRLZXqgT9bUjMR; supportWebp=true; supportwebp=true; _gid=GA1.2.54879169.1721115472; traffic_utm_referer=; Hm_lvt_f00f67093ce2f38f215010b699629083=1718809399,1719851593,1721115474; HMACCOUNT=66714B21096099E3; traffic_search_engine=; se_ref=; trkf=1; _gat_gtag_UA_199934072_2=1; _ga=GA1.1.744098953.1718809396; _ga_FZMMH98S83=GS1.1.1721115472.7.1.1721117033.0.0.0; _ga_PFYW0QLV3P=GS1.1.1721115472.7.1.1721117033.0.0.0; Hm_lpvt_f00f67093ce2f38f215010b699629083=1721117035; w_tsfp=ltvgWVEE2utBvS0Q6KjvnUqnHjg7Z2R7xFw0D+M9Os0+AaIgVZ6G1YZ9uNfldCyCt5Mxutrd9MVxYnKAV9cifRIRQMyVb5tH1VPHx8NlntdKRQJtA5zbWlZLde1w7mNFLz5cd0Cwjzx/JIdBn7IxjF1Z4SZ337ZlCa8hbMFbxl0yufqB0Jtsez+Yyw6FRUDKI2EKfeCevf5z28MDtH2KgQSgeQVhAM44gzr3q3d1CjJLt1e8A7oPRmLldbDuWJ5I5XKRvlOfK8fI0ERGuy1VpRw7UIqrgkyeOnUwIQtrZl67gLgseby3JLd3525bAf0TW1MHqQ8ZteI5+URPDSi9YHWPBfp6tQAARvJZ/82seSvF1pr+PBoKsIh9zhhy5oAP/W4gb2Ghe94JG2XCMycIeNwBPZ28MSowB0IBCTcdsxYRLjU=",
        "Referer": "https://www.qidian.com/book/1003692682/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    json_text = json.loads(response.text)
    dates = []
    volumes = json_text['data']['vs']
    for vol in volumes:
        if vol['vS']!=0:
            pass
        else:
            for chapter in vol['cs']:
                dates.append(chapter['uT'])
    return dates



if __name__ == "__main__":
  
    bookId = sys.argv[1]
    print(bookId)
    print('---------------')
    with open('data/qidianFreeChapterIds/' + bookId + '.txt') as f:
        freeChapterIds = [l.strip() for l in f.readlines()]
    dates = get_ChapterDates(bookId)
    df = pd.DataFrame({'chapterId':freeChapterIds,'date':dates})
    df.to_csv('data/qidianFreeChapterDates/' + bookId + '.csv',index=False)