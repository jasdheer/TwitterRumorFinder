#!/usr/bin/python3.4
import os, sys
import csv
import re
import time

class Tweets_list():
    def __init__(self, input_file):
        self.input = input_file
        
    def read_tweets(self):
        ##Read all the user_id entries and their tweets label
        try:
            f = open(self.input, 'r')
            next(f)
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if row[8] == 'R':
                    self.write_tweets(row, 'rumors.csv')
                elif row[8] == 'NR':
                    self.write_tweets(row, 'not_rumors.csv')
            return True
        except IOError:
            print("Error: File could not open or does not exist")
            return False

    def write_tweets(self, data, filename):
        ##Write the list of tweets in a file
        #file = open('dataset/tweets/'+filename,'a')
        #file.write(str(self.user_id[i]))
        #file.write('\n')
        
        file = csv.writer(open("dataset/tweets/"+filename, "a"), delimiter="\t")
        file.writerow(data)

class Create_File():
    def __init__(self, file):
        self.file = file
    
    def create(self):
        ##Create a dataset for the users' tweets
        file = open('dataset/tweets/'+self.file,'w')
        file.write("keyword" + '\t' + "tweet_id" + '\t' + "user_id" + '\t' + "tweet_text" + '\t' + "Date" + '\t' +"#offollowers" + '\t' + "#offriends" + '\t' + "#ofStatuses" +'\t' + "Label")
        file.write('\n')
        file.close()
        
if __name__ == '__main__':
    print("### CREATE A USER LIST ###\n")  
    filename = 'dataset/tweets.csv'
    
    fileR = Create_File('rumors.csv')
    fileR.create()
    fileNR = Create_File('not_rumors.csv')
    fileNR.create()
    
    obj = Tweets_list(filename)
    obj.read_tweets()
    
    print("Files are ready")
    time.sleep(0.5)
