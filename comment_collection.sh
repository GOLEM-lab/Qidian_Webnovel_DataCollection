!/bin/bash
var=$(cat /home/atatar/Documents/CIT/Calls/Ze/qidianBookListSample.txt)
for line in $var
do
   python qidian_data_scrape.py "${line}"
done