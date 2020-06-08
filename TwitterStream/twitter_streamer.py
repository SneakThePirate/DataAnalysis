# The purpose of this script is to stream tweets from Twitter.

import tweepy
import twitter_credentials

### Twitter Client ###
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = tweepy.API(self.auth)
        self.twitter_user = twitter_user
    
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

### TWitter Authenticator ###
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


if __name__ == '__main__':
    hash_tag_list = ['Donald Trump', 'Barrack Obama','Hillary Clinton']
    fetched_tweets_filename = 'tweets.json'

    twitter_client = TwitterClient('pycon')
    print(twitter_client.get_user_timeline_tweets(1))
    
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)