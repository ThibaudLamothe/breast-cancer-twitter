import os
import sys
import tweepy
import jsonpickle
from authenticate import *


def load_save_tweets(api, searchQuery, tweetsPerQry, file_name, maxTweets, max_id, sinceId):
    
    print("Downloading max {0} tweets".format(maxTweets))
    tweetCount = 0
    with open(file_name, 'w') as f:

        while tweetCount < maxTweets:
            try:
                # If no end limit with ID
                if (max_id <= 0):

                    # And no date limit
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang='fr', tweet_mode='extended',)
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang='fr', tweet_mode='extended', since_id=sinceId)
                
                # If number limit
                else:
                    if (not sinceId):
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang='fr', tweet_mode='extended', max_id=str(max_id - 1))
                    else:
                        new_tweets = api.search(q=searchQuery, count=tweetsPerQry, lang='fr', tweet_mode='extended', max_id=str(max_id - 1), since_id=sinceId)
                      
                # Check if Tweets have beeen found
                if not new_tweets:
                    print("No more tweets found")
                    break

                # If some, saving them
                for tweet in new_tweets:
                    f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
               
                # Update max_id
                max_id = new_tweets[-1].id
                tweetCount += 1
            except tweepy.TweepError as e:
                print("Error occured : " + str(e))
                break
    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, file_name))


if __name__ == "__main__":

    # This is what we're searching for
    search_query = '#confinement -filter:retweets'
    
    # Some arbitrary large number
    max_tweets = 10000000
    
    # this is the max the API permits 
    tweets_per_query = 100  
    
    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    since_id = None

    # If results only below a specific ID are, set max_id to that ID. (ex: max_id = 1242532002269708289)
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    # Get configuration
    config = get_config('../config.ini')
    file_name = '../data/tweets.txt'

    # Authentication
    API_KEY, API_SECRET_KEY = get_secrets(config)
    api = tweepy_authenticate(API_KEY, API_SECRET_KEY)
    check_authentication(api)

    # Make the download
    load_save_tweets(
        api=api,
        searchQuery=search_query,
        tweetsPerQry=tweets_per_query,
        file_name=file_name,
        maxTweets=max_tweets,
        max_id=max_id,
        sinceId=since_id
    )

