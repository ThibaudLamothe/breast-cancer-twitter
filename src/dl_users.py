import os
import sys
import tweepy
import jsonpickle
from authenticate import *

def load_users(users_path):
    users = []
    with open(users_path) as file:
        for cnt, line in enumerate(file):
            users.append(line)
    return users

def get_user_info(api, user_names, file_path='users.txt'):
    with open(file_path, 'w') as file:
        for user in user_names:
            user_info = api.get_user(user) 
            file.write(jsonpickle.encode(user_info._json, unpicklable=False) + '\n')


if __name__ == "__main__":

    # Users 
    users = ['ThibaudLamothe'] # Example
    users = load_users('../data/users_list.txt')

    # Parameters
    dest_file_name = 'users_twitter_data.txt'
    config = get_config('../config.ini')
    
    # Authentication
    API_KEY, API_SECRET_KEY = get_secrets(config)
    api = tweepy_authenticate(API_KEY, API_SECRET_KEY)
    check_authentication(api)

    # Downloading
    file_path = '../data/' + dest_file_name
    get_user_info(api, users, file_path=file_path)
    print('> Finished.')
    

