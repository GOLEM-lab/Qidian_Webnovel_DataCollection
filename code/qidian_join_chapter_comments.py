import os
import sys
import pandas as pd
# You can run this code for a single book or for all books using the looper.sh(bash looper.sh).
# Make sure that qidianReviews folder exists in your data folder. 

def create_Book(bookId):
    book_df = pd.DataFrame()
    for chapter in os.listdir('data/qidianReviewsByChapter/' + bookId):
        try:
            chapterId = chapter.split('.')[0]
            chapterfile = os.path.join('data/qidianReviewsByChapter/',bookId,chapter)
            chapter_df = pd.read_csv(chapterfile)
            
            chapter_df['chapterId'] =  str(chapterId)
            book_df = pd.concat([book_df,chapter_df],ignore_index=True)
        except pd.errors.EmptyDataError:
            pass
    x = book_df.shape[0]
    book_df = book_df.drop_duplicates(subset=['reviewId'])
    if book_df.shape[0]<x:
        print('Duplicates are dropped!')
    book_df = book_df.reset_index(drop=True)
    book_df.to_csv('data/qidianReviews/' + bookId + '.csv',index=False)



if __name__ == "__main__":
  
  bookId = sys.argv[1]
  print(bookId)
  print('---------------')
  create_Book(bookId)    