import sys
import pandas as pd
from glob import glob


def create_Book(bookId):
    book_df = pd.DataFrame()
    for chapter in glob('data/qidianReviews/' + bookId + '/*.csv'):
        try:
            chapter_df = pd.read_csv(chapter)
            book_df = pd.concat([book_df,chapter_df],ignore_index=True)
        except pd.errors.EmptyDataError:
            pass
    x = book_df.shape[0]
    book_df = book_df.drop_duplicates(subset=['reviewId'])
    if book_df.shape[0]<x:
        print('Duplicates are dropped!')
    book_df = book_df.reset_index(drop=True)
    book_df.to_csv('data/qidianReviewsByBook/' + bookId + '.csv',index=False)



if __name__ == "__main__":
  
  bookId = sys.argv[1]
  print(bookId)
  print('---------------')
  create_Book(bookId)    