import os
import sys
import pandas as pd

'''You can run this code multiple times. From Chapter-level reviews and replies, it creates book level reviews and replies. 
Becareful. Each time you run it it overwrites the existing file.
Duplicates are not removed. becuase the numbers on the ChapterReviewAmount.csv file includes the duplicates.'''


def create_BookReviews(bookId):
    book_df = pd.DataFrame()
    for chapter in os.listdir('data/webnovelReviews_Chapter_ByChapter/' + bookId):#this is a cvs file
        try:
            chapterfile = os.path.join('data/webnovelReviews_Chapter_ByChapter/',bookId,chapter)
            chapter_df = pd.read_csv(chapterfile,dtype={'chapterId':'str','reviewId':'str'})
            book_df = pd.concat([book_df,chapter_df],ignore_index=True)
        except pd.errors.EmptyDataError:
            pass
    #book_df = book_df.drop_duplicates(subset=['reviewId'])
    #book_df = book_df.reset_index(drop=True)
    book_df.to_csv('data/webnovelReviews_Chapter_ByBook/' + bookId + '.csv',index=False)
    print('Book saved!')


def create_BookReplies(bookId):
    book_df = pd.DataFrame()
    for chapter in os.listdir('data/webnovelReplies_Chapter_ByChapter/' + bookId):#this is a cvs file
        try:
            chapterfile = os.path.join('data/webnovelReplies_Chapter_ByChapter/',bookId,chapter)
            chapter_df = pd.read_csv(chapterfile,dtype={'chapterId':'str','reviewId':'str'})
            book_df = pd.concat([book_df,chapter_df],ignore_index=True)
        except pd.errors.EmptyDataError:
            pass
    #book_df = book_df.drop_duplicates(subset=['reviewId'])
    #book_df = book_df.reset_index(drop=True)
    book_df.to_csv('data/webnovelReplies_Chapter_ByBook/' + bookId + '.csv',index=False,)
    print('Book saved!')


if __name__ == '__main__':
    bookId = sys.argv[1]
    print(bookId)
    print('---------------')
    print('preparing reviews.')
    create_BookReviews(bookId)
    
    print('\n')
    print('preparing replies.')
    create_BookReplies(bookId)



