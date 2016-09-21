import tweepy
from tweepy import OAuthHandler
from tweepy import StreamListener
from tweepy import Stream
import configparser
import datetime

class StdOutListener(StreamListener):
    def on_data(self,data):
        #print(data)
        #tweet_lang = data.split(',"lang":"')[1].split('","timestamp_ms')[0]
        #print(tweet_lang)
        #if tweet_lang.lower() != "en":
        tweet_id = data.split(',"id_str":"')[1].split('","text')[0]
        tweet_text = data.split(',"text":"')[1].split('","source')[0]
        tweet_timestamp = data.split(',"timestamp_ms":"')[1].split('"')[0]
        
        user_info = data.split(',"user":{')[1].split('","geo')[0]
        user_id = user_info.split('"id":')[1].split(',"id_str')[0]
        user_nr_followers =  user_info.split(',"followers_count":')[1].split(',"friends_count')[0]
        user_nr_friends = user_info.split(',"friends_count":')[1].split(',"listed_count')[0]
        
        tweet_time = self.convert_timestamp(tweet_timestamp)
        
        try:
            file = open('dataset/tweets_drugs_alcohol.csv','a')
            file.write(str(tweet_time) + ',' + tweet_id + ',' + user_id + ',' + user_nr_followers + ',' + user_nr_friends + ',' + tweet_text)		
            file.write('\n')
            file.close()
            return True
        except IOError:
            print("Could not read the file")
            

    def convert_timestamp(self, timestamp):
        s = float(timestamp) / 1000.0
        time = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
        return time
        
    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    
    file = open('dataset/tweets_drugs_alcohol.csv','w')
    file.write("tweet_time" + ',' + "tweet_id" + ',' + "user_id" + ',' + "Nr of followers" + ',' + "Nr of friends" + ',' + "tweet_text")
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
