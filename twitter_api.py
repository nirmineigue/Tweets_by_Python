import tweepy
import configparser
import pandas as pd

#read configs
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#print(api_key)
# authentification

auth = tweepy.OAuth1UserHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit= True)


search_query = "'Emmanuel Macron' 'présidentielle' 'election 2022' -filter:retweets AND -filter:replies AND -filter:links"
number_of_tweets = 100

try:
    # The number of tweets we want to retrieve from search
    tweets = api.search_tweets(q=search_query, lang = "fr", count = number_of_tweets, tweet_mode = 'extended')

    # Pulling some attributes from the tweet
    attributes_container = [[tweet.user.name, tweet.created_at, tweet.favorite_count, tweet.source, tweet.full_text] for tweet in tweets]

    # Creation of column list to rename the columns in the dataframe
    columns = ["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"]

    # Creation of Dataframe
    tweets_df = pd.DataFrame(attributes_container, columns = columns)
except BaseException as e:
    print('Status Failed On', str(e))


# Save the DataFrame into a csv file
tweets_df.to_csv('tweets.csv')