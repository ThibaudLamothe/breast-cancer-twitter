import os
import sys
import tweepy
import jsonpickle
import configparser

# Load secrets
def get_config(config_path='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def get_secrets(config):
    API_KEY = config['API']['API_KEY']
    API_SECRET_KEY = config['API']['API_SECRET_KEY']
    return API_KEY, API_SECRET_KEY

# Authenticate to Tweepy
def tweepy_authenticate(API_KEY, API_SECRET_KEY):
    auth = tweepy.AppAuthHandler(API_KEY, API_SECRET_KEY)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True)
    return api

# Check authentication
def check_authentication(api):
    if (not api):
        print ("Can't Authenticate")
        sys.exit(-1)
