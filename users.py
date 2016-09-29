#!/usr/bin/python3.4
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
        self.label = []
        entries = set()
        try:
            f = open(self.input, 'r')
            next(f)
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                ##Check for double entries
                key = (row[2], row[8])
                if key not in entries:
                    self.user_id.append(row[2])
                    self.label.append(row[8])
                    entries.add(key)
            return True
        except IOError:
            print("Error: File could not open or does not exist")
            return False

    def write_users(self):
        ##Write the list of users_id in a csv file
        for i in range(0, len(self.user_id)):
            if self.label[i] == 'R':
                fr = open('dataset/users/rumor_users.csv','a')
                fr.write(str(self.user_id[i]))
                fr.write('\n')
                fr.close()
            elif self.label[i] == 'NR':
                fnr = open('dataset/users/no_rumor_users.csv', 'a')
                fnr.write(str(self.user_id[i]))
                fnr.write('\n')
                fnr.close()
        return True

if __name__ == '__main__':
    print("### CREATE A USER LIST ###\n")  
    filename = 'dataset/tweets.csv'
    
    obj = Users_list(filename)
    obj.read_users()
    obj.write_users()
    
    print("Files are ready")
    time.sleep(0.5)
