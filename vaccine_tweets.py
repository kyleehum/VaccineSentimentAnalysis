import pandas as pd
import tweepy
import re
from textblob import TextBlob
import matplotlib.pyplot as plt

#login credentials for twitter API
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

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

#calculates percentage of positive, negative, and neutral tweets
positive = df[df['Score'] == 'Positive']
print(str(positive.shape[0]/(df.shape[0])*100) + " % of positive tweets")
positive = df[df['Score'] == 'Neutral']
print(str(positive.shape[0]/(df.shape[0])*100) + " % of neutral tweets")
positive = df[df['Score'] == 'Negative']
print(str(positive.shape[0]/(df.shape[0])*100) + " % of negative tweets")

df2 = pd.read_csv("vaccine_tweets1026.csv", usecols = [4])

#applies the function to clean the tweets
df2['text'] = df2['text'].apply(cleanUpTweet)


#applies subjectivity and polarity to the tweets
df2['Subjectivity'] = df2['text'].apply(getTextSubjectivity)
df2['Polarity'] = df2['text'].apply(getTextPolarity)


#creates another column called Score and applies the function to the dataframe
df2['Score'] = df2['Polarity'].apply(getTextAnalysis)

#visualizes the data through a bar chart
labels = df2.groupby('Score').count().index.values
values = df2.groupby('Score').size().values
plt.bar(labels, values, color = ['red', 'blue', 'lime'])
plt.title(label = "Vaccine Sentiment Analysis - 12/26/2020", 
                  fontsize = '15')

#calculates percentage of positive, negative, and neutral tweets
positive = df2[df2['Score'] == 'Positive']
print(str(positive.shape[0]/(df2.shape[0])*100) + " % of positive tweets")
positive = df2[df2['Score'] == 'Neutral']
print(str(positive.shape[0]/(df2.shape[0])*100) + " % of neutral tweets")
positive = df2[df2['Score'] == 'Negative']
print(str(positive.shape[0]/(df2.shape[0])*100) + " % of negative tweets")


df3 = pd.read_csv("vaccine_tweets1028.csv", usecols = [4])

#applies the function to clean the tweets
df3['text'] = df3['text'].apply(cleanUpTweet)


#applies subjectivity and polarity to the tweets
df3['Subjectivity'] = df3['text'].apply(getTextSubjectivity)
df3['Polarity'] = df3['text'].apply(getTextPolarity)


#creates another column called Score and applies the function to the dataframe
df3['Score'] = df3['Polarity'].apply(getTextAnalysis)

#visualizes the data through a bar chart
labels = df3.groupby('Score').count().index.values
values = df3.groupby('Score').size().values
plt.bar(labels, values, color = ['red', 'blue', 'lime'])
plt.title(label = "Vaccine Sentiment Analysis - 12/28/2020", 
                  fontsize = '15')

#calculates percentage of positive, negative, and neutral tweets
positive = df3[df3['Score'] == 'Positive']
print(str(positive.shape[0]/(df3.shape[0])*100) + " % of positive tweets")
positive = df3[df3['Score'] == 'Neutral']
print(str(positive.shape[0]/(df3.shape[0])*100) + " % of neutral tweets")
positive = df3[df3['Score'] == 'Negative']
print(str(positive.shape[0]/(df3.shape[0])*100) + " % of negative tweets")

from wordcloud import WordCloud, STOPWORDS

text = ''.join([tweet for tweet in df['text']])
WordCloud = WordCloud(width=800, height=600).generate(text)
    
plt.imshow(WordCloud)
plt.show
