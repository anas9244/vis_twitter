import json

import tweepy


import pickle
import os

# access_token = "588509788-1z07dMNOMhOCw4OyLJwxSfse31TR7Aywj6h2uZgd"
# access_token_secret = "WPlTT3cpVXREXWuGvjdbxD8ie92e61vadWFlzxcoesjHe"
# consumer_key = "Em7YjncUOkyjxzZhP3hWWUDJL"
# consumer_secret = "IXkMkxVh1eFq9FJpo5vjI1NsTlzAscsEezVRjxhHZIBAnJiaEO"

access_token = "1118134186274062339-MGNkDPMhhQn0uwZlVY73T1tFvJvJ8w"
access_token_secret = "D6eXlgVJiJ5q3RQBAO03GhizanMVItD8dIZOhsBvujhUO"
consumer_key = "WC98mcJLSHMNna64T0EyzhGhV"
consumer_secret = "UKp18iWGxIZxcriW0nl1MD9b12R8fP7TIEUNb83eX1M91Vbzq9"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
fileDir = os.path.dirname(os.path.abspath(__file__))

place_tweets_file = open(fileDir + "/place_tweets.pickle", "rb")
place_tweets = pickle.load(place_tweets_file)
place_tweets_file.close()


# file_out = open("tweet.json", "w")


class TwitterListener(tweepy.StreamListener):

    def __init__(self):
        super(TwitterListener, self).__init__()

    def on_data(self, raw_data):
        try:
            tweet = json.loads(raw_data)

            if not tweet['text'].startswith('RT') and tweet['place']:
                country_code = tweet['place']['country_code']
                if country_code == 'US' and tweet['place']['place_type'] == "city":
                    state = tweet['place']['full_name'].split(', ')[1]

                    place_tweets[state] += 1

                place_tweets[country_code + '_c'] += 1
                # print(tweet['text'])

                return ("yes")
                # file_out.seek(0)
                # file_out.truncate()
                # json.dump(place_tweets, file_out)

                # def stop_streaming():
                #     print("disconnect")
                #     return False

            # return True
        except Exception as ex:

            print(ex)
            return True

    def on_error(self, status_code):
        if status_code == 420:
            print(" rate limit is reached")

            return False
        else:
            print("Error: ", status_code)
            return True

    def on_exception(self, exception):
        print("Error:", exception)


listener = TwitterListener()
twitterStream = tweepy.Stream(auth, listener)


def start_streaming(query):
    print("start")
    global place_tweets
    place_tweets = {place: 0 for place in place_tweets}
    twitterStream.filter(track=[query], is_async=True)


def get_counts():

    global place_tweets
    return (place_tweets)
