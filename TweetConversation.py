import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import time
import datetime
import urllib.request
from lxml import html
import csv

consumer_key = 'XXXXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXXX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
api = tweepy.API(auth)

file = open('dataset/conversation.csv','w')
file.write("parent_tweet_id" + '\t' + "Reply_tweet_id" + '\t' + "Original_tweet_id" + '\t' +"user_id" + '\t' + "tweet_date" + '\t' "tweet_text")
file.write('\n')
file.close()

tweet_id = ""
user_id = ""
count = 0		

with open('dataset/tweets_drugs_alcohol.csv', newline='') as f:
	next(f)
	reader = csv.reader(f, delimiter='\t')
	for row in reader:
		tweet_id = row[1]
		user_id = row[2]
		original_tweet_id = row[3]
		original_user_id = row[4]
		print ('Searching Replies for Tweet Id : '+tweet_id+ ' with Original Tweet Id : '+ original_tweet_id)
		try:
			count = count + 1
			url_str = "https://twitter.com/"+original_user_id+"/status/"+original_tweet_id
			#url_str2 = "https://twitter.com/"+user_id+"/status/"+tweet_id
			#print(url_str)
			#print(url_str2)
			f = urllib.request.urlopen(url_str)
			page = html.fromstring(f.read())
			
			reply_counter = 0
			for link in page.xpath("//a//span[2]//b"):
				time.sleep(2)
				for page2 in tweepy.Cursor(api.user_timeline, id=link.text).pages(5):
					time.sleep(1)
					for item in page2:
						if str(item.in_reply_to_status_id) == str(original_tweet_id):
							reply_counter = reply_counter + 1
							try:
								file = open('dataset/conversation.csv','a')
								file.write(str(tweet_id) + '\t' + str(item.id) + '\t' + str(original_tweet_id) + '\t' + link.text + '\t' + str(item.created_at) + '\t' + item.text)	
								file.write('\n')
								file.close()
							except IOError:
								print("Could not read the file")
			print ('Replies found for Orginal Tweet id '+original_tweet_id+' : '+ str(reply_counter))
			print ('------------------------------------------------------------------------------------------------')
			reply_counter = 0	
	
		except tweepy.TweepError as a:
			if "429" in str(a):
				print('Too many requests !!!!')
			print ('TweepyError !!!', a)
			pass

		except Exception as e:
			print ('Exception occured !!!', e)
			pass
		if count == 50:
			time.sleep(30)
			count = 0
