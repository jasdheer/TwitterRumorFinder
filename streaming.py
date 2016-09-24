#!/usr/bin/python3.4
import tweepy
from tweepy import OAuthHandler
from tweepy import StreamListener
from tweepy import Stream
import configparser
import datetime
import json
import re

class StdOutListener(StreamListener):
    def on_data(self,data):
        try:
            ##load data as json format
            data = data.replace('\\n', ' ')
            tweet_data = json.loads(data)
            tweet_lang = tweet_data['lang']
        
            if tweet_lang.lower() == "en":
                tweet_id = tweet_data['id_str']
                tweet_text = tweet_data['text']
                tweet_time = self.convert_timestamp(tweet_data['timestamp_ms'])
                
                user_id = tweet_data['user']['id_str']
                user_nr_followers = tweet_data['user']['followers_count']
                user_nr_friends = tweet_data['user']['friends_count']            
                try:
                    file = open('dataset/tweets_drugs_alcohol.csv','a')
                    file.write(str(tweet_time) + '\t' + str(tweet_id) + '\t' + str(user_id) + '\t' + str(user_nr_followers) + '\t' + str(user_nr_friends) + '\t' + tweet_text.lower())		
                    file.write('\n')
                    file.close()
                    return True
                except IOError:
                    return False
        except ValueError as error:
            return False

    def convert_timestamp(self, timestamp):
        s = float(timestamp) / 1000.0
        time = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
        return time
        
    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    
    file = open('dataset/tweets_drugs_alcohol.csv','w')
    file.write("tweet_time" + '\t' + "tweet_id" + '\t' + "user_id" + '\t' + "Nr of followers" + '\t' + "Nr of friends" + '\t' + "tweet_text")
    file.write('\n')
    file.close()
    
    l = StdOutListener()
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    consumer_key = config.get('Twitter', 'consumer_key')
    consumer_secret = config.get('Twitter', 'consumer_secret')
    access_token = config.get('Twitter', 'access_token')
    access_secret = config.get('Twitter', 'access_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    stream = Stream(auth,l)
    ##keywords that searching in tweets
    stream.filter(track = ['drug','alcohol'])
