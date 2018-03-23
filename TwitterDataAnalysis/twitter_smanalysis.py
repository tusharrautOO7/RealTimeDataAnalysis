import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from elasticsearch import Elasticsearch

# Add following key, token and secrets.
consumer_key=""
consumer_secret=""

access_token=""
access_token_secret=""

# create instance of elasticsearch
es = Elasticsearch(["localhost"], http_auth=('elastic', 'xxxx'))  # add your elasticsearch password 


class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):

        # decode json
        dict_data = json.loads(data)
        print "Original Data :%s" % dict_data
        # pass tweet into TextBlob
        tweet = TextBlob(dict_data["text"])
        print "Tweet Text : %s" % tweet
        # output sentiment polarity
        print "Sentiment : %s" % tweet.sentiment.polarity
        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"

        # output sentiment
        print "Sentiment : %s" % sentiment

        # add text and sentiment info to elasticsearch
        es.index(index="sentiment",
                 doc_type="test-type",
                 body={"author": dict_data["user"]["screen_name"],
                       "date": dict_data["created_at"],
                       "message": dict_data["text"],
                       "polarity": tweet.sentiment.polarity,
                       "subjectivity": tweet.sentiment.subjectivity,
                       "sentiment": sentiment})
        
        return True

    # on failure
    def on_error(self, status):
        print "Error : %s" % status

if __name__ == '__main__':

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    print "Done .."
    # create instance of the tweepy stream
    stream = Stream(auth, listener)
    print "Streaming started..."
    # search twitter for "modi" keyword
    stream.filter(track=['modi'])
