import os
import time
import numpy as np
import pandas as pd
'''Prepares a report on the discrapency between the collected reviews and replies and the numbers mentioned in the meat files.'''
if __name__ == '__main__':
    info = []
    with open('data/webnovelBookList.txt','r') as f:
        bookList = [x.strip() for x in f.readlines()]
    
    for bookId in bookList:
        print(bookId)
        try:
            dfMeta = pd.read_csv('data/webnovelFreeChapterMeta/'  + bookId + '.csv')
            numberTheoretical = dfMeta['reviewAmount'].sum()
        except:
            numberTheoretical = 0.0001 #to avoid division by 0
            pass
        try:
            dfReviews = pd.read_csv('data/webnovelReviews_Paragraph_ByBook/'  + bookId + '.csv')
            numberOfReviews = dfReviews.shape[0]
        except:
            numberOfReviews = 0
            pass
        try:
            dfreReplies = pd.read_csv('data/webnovelReplies_Paragraph_ByBook/' + bookId + '.csv')
            numberOfReplies = dfreReplies.shape[0]
        except:
            numberOfReplies = 0
            pass
        error = np.sqrt((numberTheoretical - (numberOfReviews + numberOfReplies))**2)/numberTheoretical
        info.append([bookId,numberOfReviews,numberOfReplies,numberOfReviews+numberOfReplies,numberTheoretical,error])

        
    dfInfo = pd.DataFrame(info,columns=['bookId','numberOfReviews','numberOfReplies','total','totalFromMeta','Discrepancy'])
    dfInfo.to_csv('data/webnovelParagraphReviewsSanityCheck.csv',index=False)