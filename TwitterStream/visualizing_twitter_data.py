# The purpose of this script is to stream tweets from Twitter.

import tweepy
import twitter_credentials
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

### Twitter Client ###
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = tweepy.API(self.auth)
        self.twitter_user = twitter_user
    
    def get_twitter_client_api(self):
        return self.twitter_client
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []

        for tweet in tweepy.Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets
    
    def get_friend_list(self, num_friends):
        friend_list = []

        for friend in tweepy.Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list
    
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []

        for tweet in tweepy.Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

### Twitter Authenticator ###
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

### Twitter Streamer ###
class TwitterStreamer():
    '''
    Class for streaming and procecssing live tweets.
    '''
    def __init__(self):
        self.twitter_autheticator = TwitterAuthenticator()
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # OAuth authorization with Twitter server.
        auth = self.twitter_autheticator.authenticate_twitter_app()

        # Set-up Twitter stream
        listener = TwitterListener(fetched_tweets_filename)
        myStream = tweepy.Stream(auth, listener)

        # Specify how you want to filter the stream
        myStream.filter(track=hash_tag_list)
    

### Twitter Stream Listener ###
class TwitterListener(tweepy.StreamListener):
    '''
    Basic listener class that prints received tweets to stdout.
    '''
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    # Prints the status
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print('Error on_data: %s' % str(e))
        return True 

    
    # If there's an error, then the method will determine if stream reconnects or stops.
    def on_error(self, status_code):
        if status_code == 420:
            # Return false data method in case Twitter limits rate.
            return False
        print(status_code)

class TweetAnalyzer():
    '''
    Functionality for analyzing and categorizing contents from tweets.
    '''
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data= [tweet.text for tweet in tweets], columns=['tweets'])
        
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['geo'] = np.array([tweet.geo for tweet in tweets])
        return df

if __name__ == '__main__':
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name='realDonaldTrump', count=200)
    # print(dir(tweets[0]))
    # print(tweets[0].retweet_count)
    
    df = tweet_analyzer.tweets_to_data_frame(tweets)

    # Get average length over all tweets.
    print(np.mean(df['len']))

    # Get the number of likes for the most liked tweet.
    print(np.max(df['likes']))

    # Get the number of retweets for the most retweeted tweet.
    print(np.max(df['retweets']))

    # Time series
    time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    time_likes.plot(figsize=(16,4), color='r')
    plt.show()