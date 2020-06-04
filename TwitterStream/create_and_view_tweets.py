# The purpose of this script is to stream tweets from Twitter.

import tweepy
import twitter_credentials

# OAuth authorization with Twitter server.
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Creates a tweet
print('\n \n ------------Creating a Tweet------------')
print('Message: This is an example for subgroup.')
api.update_status('This is an example for subgroup.')
public_tweets = api.home_timeline()

# Prints tweets
print('\n \n ------------Printing Public Tweets------------')
for tweet in public_tweets:
    print(tweet.text)