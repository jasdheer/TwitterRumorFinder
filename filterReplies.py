import csv

fileW = open('replies/filtered_replies.csv','w')
fileW.write("Matched_SearchKeyword" + '\t' +"tweet_id" + '\t' + "user_id" + '\t' "tweet_text")
fileW.write('\n')

searchKeyword = ""
with open('replies/rumour_keywords.csv', newline='') as f2:
    #next(f2)
    reader = csv.reader(f2, delimiter='\t')
    for row in reader:
        searchKeyword = row[0]
        searchKeyword_lowerCase = searchKeyword.lower()
        
        f = open("replies/replies.csv", "r")
        print("\n---------------------------------")
        for line in f:
            line_lowerCase = line.lower()
            if searchKeyword_lowerCase in line_lowerCase:
                try:
                    fileW.write(searchKeyword+'\t'+line); 
                except IOError:
                    print("Could not read the file")
        print("Search completed for : "+str(searchKeyword))
print("\n---------------------------------")
print("Filtered replies are now in file : replies/filtered_replies.csv\n")
f.close()
fileW.close()
