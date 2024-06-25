import os
import time
import requests
import numpy as np
import pandas as pd
from tqdm.auto import tqdm


def get_CollectionProcessSummary(bookId):
    #read the list of free chapters
    with open('data/qidianFreeChapterIds/' + bookId + '.txt',"r") as f:
        chapterIds = [b.strip() for b in f.readlines()] # this is a string
    bookCommentSummary = pd.read_csv('data/qidianFreeChapterMeta/' + bookId + '.csv')
    metaChapterIds = bookCommentSummary["qidianChapterId"].apply(str).unique()
    #get the list of collected chapters:
    fileList = os.listdir('data/qidianReviews/' + bookId)
    collectedIds = [file.split('.')[0] for file in fileList]
    missingIds = [id for id in metaChapterIds if id not in collectedIds]
    noCommentIds = [id for id in chapterIds if id not in metaChapterIds]
    #qidianBookId,numOfChapters,numOfCollectedChapters,completionPercentage,missingIds,noCommentIds
    return (id,len(chapterIds),len(metaChapterIds),len(collectedIds),len(collectedIds)/(len(metaChapterIds))*100,missingIds,noCommentIds)

if __name__ == "__main__":

    bookList = pd.read_csv('data/bookList.csv')
    bookList = bookList.dropna(subset=['qidianUrl'])
    qidianBookIds = bookList['qidianBookId']
    summary = []
    for id in qidianBookIds:
        if id != 3447263:
            id = str(int(id))
            summary.append(get_CollectionProcessSummary(id))

    summary_df = pd.DataFrame(summary,columns=['qidianBookId','numOfChapters','numberOfChaptersWithComments','numOfCollectedChapters','completionPercentage','missingChapterIds','noCommentChapterIds'])
    summary_df = summary_df.sort_values('completionPercentage',ascending=False)
    summary_df.to_csv('data/collectionProgress_' + str(pd.Timestamp.today()) + '.csv',index=False)