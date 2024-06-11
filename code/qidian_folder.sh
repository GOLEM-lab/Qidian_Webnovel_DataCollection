!/bin/bash
var=$(cat /home/atatar/Documents/CIT/Calls/Ze/qidianBookList.txt)
for line in $var
do
   mkdir "${line}"
done
