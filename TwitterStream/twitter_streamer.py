# The purpose of this script is to stream tweets from Twitter.

import tweepy
import twitter_credentials


class MyStreamListener(tweepy.StreamListener):
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
        print(status_code)

class TwitterStreamer():
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # OAuth authorization with Twitter server.
        auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        # Set-up Twitter stream
        myStreamListener = MyStreamListener(fetched_tweets_filename)
        myStream = tweepy.Stream(auth = api.auth, listener = myStreamListener)

        # Specify how you want to filter the stream
        myStream.filter(track=hash_tag_list)
    
if __name__ == '__main__':
    hash_tag_list = ['Donald Trump', 'Barrack Obama','Hillary Clinton']
    fetched_tweets_filename = 'tweets.json'

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)