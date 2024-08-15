import os
import sys
import pandas as pd

'''You can run this code multiple times. It first creates the chapters. Once all chapters are created it creates the book. 
Becareful. Each time you run it it overwrites the existing file.'''

def create_Chapter(bookId,chapterId):
    chapter_df = pd.DataFrame()
    for paragraph in os.listdir('data/webnovelReviews_Paragraph_ByParagraph/' + bookId + '/' + chapterId):
        try:
            paragraphfile = os.path.join('data/webnovelReviews_Paragraph_ByParagraph/',bookId, chapterId,paragraph)
            paragraph_df = pd.read_csv(paragraphfile,dtype={'chapterId':'str','paragraphId':'str','reviewId':'str'})
            chapter_df = pd.concat([chapter_df,paragraph_df],ignore_index=True)
        except pd.errors.EmptyDataError:
            pass
    chapter_df = chapter_df.drop_duplicates(subset=['reviewId'])

    print('Chapter createad successfully!')
    print('************')
    chapter_df = chapter_df.reset_index(drop=True)
    chapter_df.to_csv('data/webnovelReviews_Paragraph_ByChapter/' + bookId + '/' + chapterId + '.csv',index=False)


def create_Book(bookId):
    book_df = pd.DataFrame()
    for chapter in os.listdir('data/webnovelReviews_Paragraph_ByChapter/' + bookId):#this is a cvs file
        try:
            chapterfile = os.path.join('data/webnovelReviews_Paragraph_ByChapter/',bookId,chapter)
            chapter_df = pd.read_csv(chapterfile,dtype={'chapterId':'str','reviewId':'str'})
            book_df = pd.concat([book_df,chapter_df],ignore_index=True)
        except pd.errors.EmptyDataError:
            pass
    book_df = book_df.drop_duplicates(subset=['reviewId'])
    book_df = book_df.reset_index(drop=True)
    book_df.to_csv('data/webnovelReviews_Paragraph_ByBook/' + bookId + '.csv',index=False,)
    print('Book saved!')



if __name__ == '__main__':
    bookId = sys.argv[1]
    print(bookId)
    print('---------------')

    dfMeta = pd.read_csv('data/webnovelFreeChapterMeta/' + bookId + '.csv',dtype={'chapterId':'string'})
    chapterIds = dfMeta['chapterId'].unique()
    collectedChapterIds = [x.split('.')[0] for x in os.listdir('data/webnovelReviews_Paragraph_ByChapter/' + bookId + '/')]
    print('Number of Collected Chapters',len(collectedChapterIds))
    missingChapterIds = [x for x in chapterIds if x not in collectedChapterIds]
    print('Number of Missing Chapters',len(missingChapterIds))
    print('____________')

    if len(missingChapterIds) != 0:
        print('chapters are not complete! Creating chapters')
        for chapterId in missingChapterIds:
            paragraphIds = dfMeta['paragraphId'][dfMeta['chapterId'] == chapterId]
            collectedParagraphIds = [x.split('.')[0] for x in os.listdir('data/webnovelReviews_Paragraph_ByParagraph/' + bookId + '/' + chapterId + '/')]
            missingParagraphIds = [x for x in paragraphIds if x not in collectedParagraphIds]
            if len(missingParagraphIds) == 0:
                create_Chapter(bookId,chapterId)
    else:
        print('all chapters are complete. preparing the book.')
        print('\n')
        create_Book(bookId)



