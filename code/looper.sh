!/bin/bash
#var=$(cat /home/atatar/Documents/CIT/Calls/Ze/data/qidianBookList.csv)
var=$(cat /home/atatar/Documents/CIT/Calls/Ze/data/webnovelBookList.txt)
for line in $var
do
   #select the operation you want to accomplish: collect reviews, join chapters, collect replies
   
   #python code/qidian_review_scrape.py "${line}"
   #python code/qidian_join_chapter_comments.py "${line}"
   #python code/qidian_reply_scrape.py "${line}"
   #python code/qidian_chapter_date_scrape.py "${line}"
   #python code/webnovel_ChapterReview_scrape.py "${line}"
   #python code/webnovel_join_comments.py "${line}"
   #python code/webnovel_ChapterReview_scrape_patch.py "${line}"
   #python code/webnovel_join_with_addendum.py "${line}"
   #python code/webnovel_ChapterReplies_scrape.py "${line}"
   # you can also use this to create folders for every book
   #mkdir data/webnovelReviews_ChapterByChapterByParagraph_Addendum/"${line}"
done