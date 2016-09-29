#!/usr/bin/python3.4
import tweepy
from tweepy import OAuthHandler
from langdetect import detect
import langdetect
from glob import glob
import configparser
import csv
import time,  datetime

class Retrieve_Tweets():
    def __init__(self, file, keyword):
        self.file = file
        self.keyword = keyword
        
    def retrieve(self):
        self.user_id = []
        try:
            f = open('dataset/'+self.file, 'r')
            reader = csv.reader(f)
            for row in reader:
                self.user_id.append(row[0])
        except IOError:
            print("Error: File could not open or does not exist")
            return False
        
        count_tweets = 0;
        count_keyword_tweets = 0;
        for i in range(0, len(self.user_id)): 
            user = self.user_id[i]
            try:
                for tweet in tweepy.Cursor(api.user_timeline, id=user, lang = 'en').items(100):
                    #count_tweets += 1
                    #print(count_tweets)
                    try:
                        if (detect(tweet.text) == 'en'):
                            if self.keyword in tweet.text:
                                count_keyword_tweets +=1
                                print(count_keyword_tweets)
                                self.on_data(tweet)
                    except langdetect.lang_detect_exception.LangDetectException as e:
                        pass
            except tweepy.TweepError as a:
                print('TweepyError!!!')
                if "429" in str(a):
                    print('Too many requests!!!')
                    print ('Please wait ...... It will continue itself after 15 minutes.')
                    print ('Current Time : '+ str(datetime.datetime.now().time()))
                    time.sleep(60*15)                
                pass

    def on_data(self, data):
        ##Get the language from twitter data
        tweet_lang = data.lang

        ##Get the tweet ID, text and posted time
        tweet_id = data.id
        tweet_text = data.text
        tweet_text = tweet_text.replace('\n', ' ')
        tweet_text = tweet_text.replace('\\n', ' ')
        tweet_time = data.created_at
        
        ##Get the user ID, number of followers and friends
        user_id = data.user.id
        user_nr_followers = data.user.followers_count
        user_nr_friends = data.user.friends_count

        ##If it is retweet, get the original tweet id and user id
        try:
            original_tweet_id = data.retweeted_status.id
            original_user_id = data.retweeted_status.user.id
        except Exception as e:
            original_tweet_id = tweet_id
            original_user_id = user_id

        ##Write the data in a csv file
        try:
            file = open('dataset/input/tweets_of_'+ self.file,'a')
            file.write(str(tweet_time) + '\t' + str(tweet_id) + '\t' + str(user_id) + '\t' + str(original_tweet_id) + '\t' + str(original_user_id) +  '\t' + str(user_nr_followers) + '\t' + str(user_nr_friends) + '\t' + tweet_text.lower())
            file.write('\n')
            file.close()
            return True
        except IOError:
            return False

class Create_File():
    def __init__(self, file):
        self.file = file
    
    def create(self):
        ##Create a dataset for the users' tweets
        file = open('dataset/input/tweets_of_' + self.file,'w')
        file.write("tweet_time" + '\t' + "tweet_id" + '\t' + "user_id" + '\t' + "original_tweet_id" + '\t' + "original_user_id" + '\t' +"#offollowers" + '\t' + "#offriends" + '\t' + "tweet_text")
        file.write('\n')
        file.close()
        

if __name__ == '__main__':
    print("### SEARCH THE TWEETS OF USERS FOR A SPECIFIC WORD ###\n")
    
    ##establish the connection with the twitter api by reading credentials from config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    consumer_key = config.get('Twitter', 'consumer_key')
    consumer_secret = config.get('Twitter', 'consumer_secret')
    access_token = config.get('Twitter', 'access_token')
    access_secret = config.get('Twitter', 'access_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    
    ##Create output files
    fileR = Create_File('rumor_users.csv')
    fileR.create()
    #fileNR = Create_File('no_rumor_users.csv')
    #fileNR.create()
    
    keyword = input('Please, insert the keyword: ')
    obj = Retrieve_Tweets('rumor_users.csv', keyword)
    obj.retrieve()
