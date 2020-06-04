# The purpose of this script is to stream tweets from Twitter.

import tweepy
import twitter_credentials

# 
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

api.update_profile('Sentiment Analysis Beta Test')
public_tweets = api.home_timeline()

for tweet in public_tweets:
    print(tweet.text)