# The purpose of this script is to stream tweets from Twitter.

import tweepy
import twitter_credentials

'''
The MyStreamListener classifies twitter messages and routes them to appropiately named methods.
'''
class MyStreamListener(tweepy.StreamListener):
    # Prints the status
    def on_status(self, status):
        print(status.text)
    
    # If there's an error, then the method will determine if stream reconnects or stops.
    def on_error(self, status_code):
        if status_code == 420:
            return False

# OAuth authorization with Twitter server.
auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Set-up Twitter stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)

# Specify how you want to filter the stream
myStream.filter(track=['COVID'])