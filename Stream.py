import json
import os.path
import tweepy
import glob
import os

import datetime
import main


access_token = "1118134186274062339-MGNkDPMhhQn0uwZlVY73T1tFvJvJ8w"
access_token_secret = "D6eXlgVJiJ5q3RQBAO03GhizanMVItD8dIZOhsBvujhUO"
consumer_key = "WC98mcJLSHMNna64T0EyzhGhV"
consumer_secret = "UKp18iWGxIZxcriW0nl1MD9b12R8fP7TIEUNb83eX1M91Vbzq9"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


class TwitterListener(tweepy.StreamListener):

    def __init__(self):
        super(TwitterListener, self).__init__()
        self.num_tweets = 0
        self.valid = False

        self.file_index = 0
        self.file = set_file(self.file_index)

    def on_data(self, raw_data):
        try:
            json_data = json.loads(raw_data)
            if valid_chk(json_data):
                if self.num_tweets >= 36347:
                    return False
                self.num_tweets += 1

                # Write to new file every 100K tweet
                if self.num_tweets % 100000 == 0:
                    currentDT = datetime.datetime.now()
                    log_stuff("number of tweets: " +
                              str(self.num_tweets) + ", Time: " + str(currentDT))

                    # Write last tweet out of 100K to the current file; otherwise it would be 99999
                    json.dump(json_data, self.file, ensure_ascii=False)

                    # Close current file
                    self.file.close()
                    # increment filename for next 100K tweets
                    self.file_index += 1
                    self.file = set_file(self.file_index)
                    print(self.num_tweets)

                # elif self.num_tweets <= 1000000:

                else:
                    json.dump(json_data, self.file, ensure_ascii=False)
                    self.file.write("\n")
                    print(raw_data)

                # else:
                #     print("Finished!", self.num_tweets)
                #     return False
                return True
        except Exception as ex:
            log_stuff("Unhandled exception from on_status: " + str(ex))
            print(ex)
            return True

    def on_error(self, status_code):
        if status_code == 420:
            print(" rate limit is reached")
            with open("log.txt", 'w') as file:
                file.write("rate limit is reached")
            return False
        else:
            log_stuff("status code error: " + str(status_code))

            print("Error: ", status_code)
            return True

    def on_exception(self, exception):
        print("Error:", exception)

        log_stuff("on_exception error: " + str(exception))
