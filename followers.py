#!/usr/bin/python3.4
##Create a list with the followers and friends of a user who is in the rumor_users.csv file

from tweepy import OAuthHandler
import tweepy
import configparser
import os, sys
import csv
import re
import time

class Users_list():
    def __init__(self, input_file):
        self.input = input_file
        
    def read_users(self):
        ##Read all the user_id entries and their tweets label
        self.user_id = []
        try:
            f = open(self.input, 'r')
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                self.user_id.append(row[0])
            return True
        except IOError:
            print("Error: File could not open or does not exist")
            return False

    def write_ff(self):
        for i in range(0, len(self.user_id)):
            self.write_followers(self.user_id[i])
            self.write_friends(self.user_id[i])

    def write_followers(self, user):
        ##Write the list of followers in a new csv file
        fo = open('dataset/users/followers_of_rumor_users.csv','a')
        try:
            for follower in tweepy.Cursor(api.followers_ids, id=user).items(200):
                fo.write(str(user) + '\t' + str(follower))
                fo.write('\n')
        except tweepy.TweepError as a:
            print('TweepyError!!!')             
            pass
        fo.close()
        return True

    def write_friends(self, user):
        ##Write the list of friends in a new csv file
        fr = open('dataset/users/friends_of_rumor_users.csv','a')
        try:
            for follower in tweepy.Cursor(api.friends_ids, id=user).items(200):
                fr.write(str(user) + '\t' + str(follower))
                fr.write('\n')
        except tweepy.TweepError as a:
            print('TweepyError!!!')             
            pass
        fr.close()
        return True
        
        
class Create_File():
    def __init__(self, file):
        self.file = file
    
    def create(self):
        ##Create a dataset for the users' tweets
        file = open('dataset/users/' + self.file,'w')
        file.write("user_id" + '\t' + "follower_id" )
        file.write('\n')
        file.close()

if __name__ == '__main__':
    print("### CREATE A FOLLOWER LIST ###\n") 
    filename = 'dataset/users/rumor_users.csv' #Change the way that it reads the file
    
    ##establish the connection with the twitter api by reading credentials from config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    consumer_key = config.get('Twitter', 'consumer_key')
    consumer_secret = config.get('Twitter', 'consumer_secret')
    access_token = config.get('Twitter', 'access_token')
    access_secret = config.get('Twitter', 'access_secret')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth,  wait_on_rate_limit = True,  wait_on_rate_limit_notify = True)
    
    fileFoR = Create_File('followers_of_rumor_users.csv')
    fileFoR.create()
    fileFroR = Create_File('friends_of_rumor_users.csv')
    fileFroR.create()
    
    obj = Users_list(filename)
    obj.read_users()
    obj.write_ff()
    
    print("Files are ready")
    time.sleep(2)
