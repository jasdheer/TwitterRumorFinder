#!/usr/bin/python3.4
##Lower case (done in search procedure)
##Remove emojis (done)
##Remove stop words (done)
##Remove urls and @users (done)
##Remove short words (to be done)
##Token (done)
##Stemming (done, but need to be improved)
##Spell Checking ????
##Check for multiple inputs

from nltk.corpus import stopwords
from stemming.porter2 import stem
import os, sys
import csv
import re
import time

class Tweets():
    def __init__(self, input_file):
        self.input = input_file

    def read_tweets(self):
        ##Read all the tweets and save them in a list, which is returned to the main process
        self.tweet_text = []
        try:
            f = open(self.input, 'r')
            next(f)
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                ##Check for double entries
                self.tweet_text.append(row[3])
            return self.tweet_text
        except IOError:
            print("Error: File could not open or does not exist")
            return False

class Methods():
    def __init__(self):
        self.stop = set(stopwords.words('english'))
        ##By http://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
        self.emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"!,$,%,^,&,*,.,?"
                           "]+", flags=re.UNICODE)

    def remove_emojis(self, tweet):
        tw_w_em = self.emoji_pattern.sub(r'', tweet)
        return tw_w_em
    
    def remove_urls(self, tweet):
        tweet = re.sub(r"(http?\://)\S+", "", tweet)
        tweet = re.sub(r"(https?\://)\S+", "", tweet)
        tweet = re.sub(r"(?:\@|\#|//)\S+", "", tweet)
        return tweet
        
    def remove_stop_words(self, tweet):
        no_stop_words = []
        for word in tweet.split():
            if word not in self.stop:
                no_stop_words.append(word)        
        return(no_stop_words)

    def stemming(self, list):
        stem_list = []
        for word in list:
            stem_list.append(stem(word))
        return stem_list

##Create a file and append it with the tokens for each tweet
class Create_File():
    def __init__(self, file):
        self.file = file
    
    def create(self):
        ##Create a dataset for the users' tweets
        file = open('dataset/tokens/tokens_of_' + self.file,'w')
        file.close()
        
    def append(self, tokens):
        file = open('dataset/tokens/tokens_of_'+self.file, 'a')
        writer = csv.writer(file, delimiter = '\t')
        writer.writerow(tokens)


if __name__ == '__main__':
    print("### PRE-PROCESSING PROCEDURE ###\n")  
    
    ##Get the tweets from the file and save them in a list
    filename = 'dataset/tweets/rumors.csv'
    obj = Tweets(filename)
    tweets = obj.read_tweets()


    token_list = []
    proc = Methods()
    
    ##For each tweet call the functions to remove urls, emojis and stop_words
    ##remove_stop_words, split the tweet in token words
    for i in range(0, len(tweets)):
        tweets[i] = proc.remove_urls(tweets[i])
        tweets[i] = proc.remove_emojis(tweets[i])
        token_list.append(proc.remove_stop_words(tweets[i]))

    ##Stem the token words
    for i in range(0, len(token_list)):
        token_list[i] = proc.stemming(token_list[i])
    
    ##Create a new file in tokens folder
    ##Save the tokens for each tweet
    cf = Create_File('rumors.csv')
    cf.create()
    
    for list in token_list:
        cf.append(list)

    print("File is ready")
    time.sleep(0.5)
