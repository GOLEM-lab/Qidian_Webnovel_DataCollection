import os
import re
import sys
import json
import time
import numpy as np
import pandas as pd

def get_MissingChapters(bookId):
    #get the list of free chapters
    with open('../data/qidianFreeChapterIds/' + bookId + '.txt',) as f:
        chapterIds = [b.strip() for b in f.readlines()]
    #get the list of collected chapters:
    fileList = os.listdir('../data/qidianReviews/' + bookId)
    collectedIds = [file.split('.')[0] for file in fileList]
    missingIds = [id for id in chapterIds if id not in collectedIds]
    #qidianBookId,numOfChapters,numOfCollectedChapters,completionPercentage,missingChapterIds
    return (id,len(chapterIds),len(collectedIds),len(collectedIds)/len(chapterIds)*100,missingIds)


if __name__ == "__main__":
    bookList = pd.read_csv('../data/bookList.csv')
    bookList = bookList.dropna(subset=['qidianUrl'])
    qidianBookIds = bookList['qidianBookId']
    summary = []
    for id in qidianBookIds:
        id = str(int(id))
        summary.append(get_MissingChapters(id))

    summary_df = pd.DataFrame(summary,columns=['qidianBookId','numOfChapters','numOfCollectedChapters','completionPercentage','missingChapterIds'])
    summary_df = summary_df.sort_values('completionPercentage',ascending=False)
    summary_df.to_csv('../data/collectionProgress_' + str(pd.Timestamp.today()) + '.csv',index=False)