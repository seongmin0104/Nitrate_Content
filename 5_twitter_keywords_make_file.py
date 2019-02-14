# Import package
import tweepy, json

# Store OAuth authentication credentials in relevant variables
access_token = "1011919974745673729-YtF630JZLi47cdTAXjVPpvH7q6VzFb"
access_token_secret = "2L7p1PUpZTneQsDXclWj4vuvtQcfWlTb8DidfGPuadoCI"
consumer_key = "c52uQ96uYXDGrWZ7yVTIMu36K"
consumer_secret = "6w3HCsDCnDB9SQFI8w9nlc6Tf3xEq7cmh6SyryMWhvDxvAGhN8"

# Pass OAuth details to tweepy's OAuth handler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open("tweet_sad_happy.txt", "w")

    def on_status(self, status):
        tweet = status._json
        self.file.write( json.dumps(tweet) + '\n')
        self.num_tweets += 1
        if self.num_tweets < 1000:
            return True
        else:
            return False
        self.file.close()

    def on_error(self, status):
        print(status)

l = MyStreamListener()
stream = tweepy.Stream(auth, l)

#this line filters Twitter streams to capture data by keywords:
stream.filter(track=['sad','happy'])
