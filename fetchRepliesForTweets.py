#!/usr/bin/python3.4
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import time
import datetime
import urllib.request
from lxml import html
import csv
import configparser
import sys
import os

def conv_search(api):
    file = open('replies/replies.csv','w')
    file.write("Original_Tweet_Id" + '\t' + "User_Id" + '\t' + "User_Name" + '\t' +"Reply_User_Id" + '\t' +"Reply_User_Name" + '\t' "Tweet_Text")
    file.write('\n')
    file.close()

    file2 = open('replies/replies_ignored_info.csv','w')
    file3 = open('replies/replies_exceptions.csv','w')
    
    tweet_id = ""
    tweet_list = []		

    dirPath = 'input/' 
    files = os.listdir(dirPath)
    # Note that input file contain only 1 csv file
    if len(files) > 1:
        print('\nOnly single tweet csv file must be present in the input directory !!!  \n')
        return
    filePath = dirPath + str(files[0])

    # Get Tweet Ids and other information from the tweet input file
    with open(filePath, newline='') as f:
        next(f)
        reader = csv.reader(f, delimiter='\t')
        file = open('replies/replies.csv','a')
        for row in reader:
            tweet_id = row[1]
            original_tweet_id = row[3]
            original_user_id = row[4]
            reply_counter = 0
            # Original tweet id if scanned alredy will not be scanned again.
            if str(original_tweet_id) in tweet_list:
                try:
                    file2.write(str(tweet_id)+" corresponds to the original tweet id :"+str(original_tweet_id) +" which has been already covered, hence "+str(tweet_id)+" is ignored")	
                    file2.write('\n')
                except IOError:
                    print("Could not read the file")
         
            print ('------------------------------------------------------------------------------------------------\n')
            print ('Searching Replies for Tweet Id : '+tweet_id+ ' with Original Tweet Id : '+ original_tweet_id)
            #Parse the url and get the info like, replies, replied usernames, hashtags etc
            try:
                tweet_list.append(original_tweet_id)
                url_str = "https://twitter.com/"+original_user_id+"/status/"+original_tweet_id
                f = urllib.request.urlopen(url_str)
                page = html.fromstring(f.read())
                
                user_path = ".//*[@id='page-container']/a/@href"
                original_user_display_name = ""
                for user_link in page.xpath(user_path):
                    original_user_text = str(user_link)
                    original_user_text = original_user_text.replace('/', '@')
                    original_user_display_name = str(original_user_text)
                
                path = ".//*[@class='stream-items js-navigable-stream']/div"
                i = 1
                for link1 in page.xpath(path):
                    user_path = "../div["+str(i)+"]/li/div/div[2]/div[1]/a/span[2]/b/text()"
                    user_name = link1.xpath(user_path)
                    user_name = "@"+str(user_name[0])
                    user_id_path = "../div["+str(i)+"]/li/div/div[2]/div[1]/a/@data-user-id"
                    userID = link1.xpath(user_id_path)
                    userID = userID[0]
                    tweet_text = ""
                    inner_counter = 1
                    tweet_nr = 4
                    for link in page.xpath(".//*[@class='stream-items js-navigable-stream']/div["+str(i)+"]/li/div/div[2]/div[2]/p/child::node()"):
                        if not hasattr(link, 'text') and str(link) !="" :
                            tweet_text = tweet_text +" "+ str(link)
                        elif 'Element a' in str(link) and 'None'in str(link.text) :
                            tagged_user_sign = "../../../../../../../div["+str(i)+"]/li/div/div[2]/div[2]/p/child::node()["+str(inner_counter)+"]/s/text()"
                            tagged_user_sign_text = link.xpath( tagged_user_sign)
                            tagged_user_name = "../../../../../../../div["+str(i)+"]/li/div/div[2]/div[2]/p/child::node()["+str(inner_counter)+"]/b/text()"
                            tagged_user_name_text = link.xpath( tagged_user_name)
                            tweet_text = tweet_text + tagged_user_sign_text[0] + tagged_user_name_text[0]
                        elif 'Element a' in str(link) and 'pic'in str(link.text) :
                            tweet_text = tweet_text +" "+ str(link.text)
                        inner_counter = inner_counter + 1
                    inner_counter = 1
                    # write the gathered info in file
                    try:
                        text = str(tweet_text)
                        text = text.replace('\n', ' ')
                        text = text.replace('\\n', ' ')
                        file.write(str(original_tweet_id)  + '\t' + str(original_user_id) +'\t'+ original_user_display_name+'\t'+ str(userID) + '\t'+str(user_name)+'\t' + text.lower())	
                        file.write('\n')
                        reply_counter = reply_counter + 1
                    except IOError:
                        print("Could not read the file")

                    i  = i + 1
                i = 0  

                print ('\nReplies found for Orginal Tweet id '+original_tweet_id+' : '+ str(reply_counter))
                reply_counter = 0	
                
            except Exception as e:
                print ('Exception occured and has been logged in exception file!!!', e)
                # Process must not stop for any exception thrown by a particular tweet. That tweet id will be logged in a file and will be checked manually
                try:
                    file3.write("Exception occured for "+str(original_tweet_id)+" Check this tweet manually.")	
                    file3.write('\n')
                except IOError:
                    print("Could not read the file")
                pass
 
        file.write('\n\n')
        file.close()
        file2.write('\n\n')
        file2.close()
        file3.write('\n\n')
        file3.close()
        print("Replies are now in file : replies/replies.csv")    
        
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    consumer_key = config.get('Twitter', 'consumer_key')
    consumer_secret = config.get('Twitter', 'consumer_secret')
    access_token = config.get('Twitter', 'access_token')
    access_secret = config.get('Twitter', 'access_secret')
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    conv_search(api)
