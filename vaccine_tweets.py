import pandas as pd
import tweepy
import re
from textblob import TextBlob
import matplotlib.pyplot as plt

#login credentials for twitter API
consumer_key = "EvSt1PFSOIxLc0IgHBD5xpC5A"
consumer_secret = "4711ElaUe6KalAEKQuUZnrG3uXtBxf4mH0IxuN8fIsTK5BDbLO"
access_token = "1182850072565837824-SsVIUnKh7dfcFSAyBBUSh9fxUct1Bs"
access_token_secret = "uwrlviI9gBaTJYwbg9qEciUDSJRwIRKvjsOBJ7abZodul"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth) 

#extracts the most recent 500 tweets containing the keyword vaccine from the Twitter API
results = api.search(q='vaccine', count=500)
#converts the json output to a dataframe saved as a CSV file
json_data = [r._json for r in results]
df = pd.json_normalize(json_data)
df.to_csv('vaccine_tweets.csv')


for tweet in tweepy.Cursor(api.search,q="vaccine",count=200,
                           lang="en",
                           since="2020-12-17").items(200):
    print(tweet.text)

#loads the CSV file and selects only the column revelant to this analysis
df = pd.read_csv("vaccine_tweets.csv", usecols = [4])

#creates a function to remove all @'s, hashtags, and links
#Then applies it to the dataframe
def cleanUpTweet(txt):
    # Remove mentions
    txt = re.sub(r'@[A-Za-z0-9_]+', '', txt)
    # Remove hashtags
    txt = re.sub(r'#', '', txt)
    # Remove retweets:
    txt = re.sub(r'RT : ', '', txt)
    # Remove urls
    txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', txt)
    return txt
df['text'] = df['text'].apply(cleanUpTweet)

#creates a function that determines subjectivity and polarity from the textblob package
def getTextSubjectivity(txt):
    return TextBlob(txt).sentiment.subjectivity
def getTextPolarity(txt):
    return TextBlob(txt).sentiment.polarity

#applies these functions to the dataframe
df['Subjectivity'] = df['text'].apply(getTextSubjectivity)
df['Polarity'] = df['text'].apply(getTextPolarity)

#builds a function to calculate and categorize each tweet ad Negative, Neutral, and Positive
def getTextAnalysis(a):
    if a < 0:
        return "Negative"
    elif a == 0:
        return "Neutral"
    else:
        return "Positive"

#creates another column called Score and applies the function to the dataframe
df['Score'] = df['Polarity'].apply(getTextAnalysis)

#visualizes the data through a bar chart
labels = df.groupby('Score').count().index.values
values = df.groupby('Score').size().values
plt.bar(labels, values, color = ['red', 'blue', 'lime'])
