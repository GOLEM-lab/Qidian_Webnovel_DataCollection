!/bin/bash
var=$(cat /home/atatar/Documents/CIT/Calls/Ze/qidianBookList.txt)
for line in $var
do
   #select the operation you want to accomplish: collect reviews, join cahpters, collect replies
   #python code/qidian_data_scrape.py "${line}"
   #python code/qidian_join_chapter_comments.py "${line}"
   python code/qidian_reply_scrape.py "${line}"
done