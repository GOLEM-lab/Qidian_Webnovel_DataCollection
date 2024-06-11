import os
import time
import requests
import numpy as np
import pandas as pd
from tqdm.auto import tqdm


def get_CollectionProcessSummary(bookId):
    #read the list of free chapters
    with open('data/qidianFreeChapterIds/' + bookId + '.txt',"r") as f:
        chapterIds = [b.strip() for b in f.readlines()]
    #record the chapters with no comments
    noCommentPath = 'data/qidianNoCommentChapterIds/' + bookId + '.txt'
    if os.path.isfile(noCommentPath) :
        with open(noCommentPath,'r') as f:
            noCommentIds = [b.strip() for b in f.readlines()]
    else:
        noCommentIds = []
    #get the list of collected chapters:
    fileList = os.listdir('data/qidianReviews/' + bookId)
    collectedIds = [file.split('.')[0] for file in fileList]
    processedIds = collectedIds + noCommentIds
    missingIds = [id for id in chapterIds if id not in processedIds]
    #qidianBookId,numOfChapters,numOfCollectedChapters,completionPercentage,missingIds,noCommentIds
    return (id,len(chapterIds),len(collectedIds),len(collectedIds)/(len(chapterIds) - len(noCommentIds))*100,missingIds,noCommentIds)

if __name__ == "__main__":

    bookList = pd.read_csv('data/bookList.csv')
    bookList = bookList.dropna(subset=['qidianUrl'])
    qidianBookIds = bookList['qidianBookId']
    summary = []
    for id in qidianBookIds:
        id = str(int(id))
        summary.append(get_CollectionProcessSummary(id))

    summary_df = pd.DataFrame(summary,columns=['qidianBookId','numOfChapters','numOfCollectedChapters','completionPercentage','missingChapterIds','noCommentChapterIds'])
    summary_df = summary_df.sort_values('completionPercentage',ascending=False)
    summary_df.to_csv('data/collectionProgress_' + str(pd.Timestamp.today()) + '.csv',index=False)