# VaccineSentimentAnalysis

## Background Information
The purpose behind this project was to evaluate and analyze the general opinion of the most recently introduced COVID19 vaccine.  In order to gather the public's opinion, the most recent tweets from 12/10/2020 were extracted from Twitter's API.  This analysis will utilize data cleaning and manipulating, natural language processing (NLP), and data visualization.

### Packages utilized: Pandas, Tweepy, TextBlob, RE, and Matplotlib

## Overview
Once obtaining a Twitter Developer account, I was able to access their API.  With access to their API, I extracted the most recent tweets containing the keyword "vaccine".  The output results in a JSON file that I converted to a dataframe and saved as a CSV file.  In order to clean the data, the CSV file was loaded and selected only the columns relevant to this analysis, text or user's tweets.  Then a function was created and applied to remove all the @'s, hashtags, and links from the dataframe.  Once the data was cleaned, a function was created, from the TextBlob package, to determine the subjectivity and polarity.  Polarity is essential as it evaluates the emotions expressed in the tweet.  A polarity of greater than 0 indicates a positive sentiment, a polarity of exactly 0 equals a neutral sentiment, and a polarity of less than 0 indicates a negative sentiment.  With the polarity and subjectivity calculated, a new column was created and applied to categorize each tweet into their appropriate categories.  Lastly, the data was visualized through a bar chart

## Results
The analysis indicated a sentiment of 40% positive tweets, 48% neutral tweets, and 12% negative tweets.  As shown below in the visualization, the general opinion of the vaccine, as of December 2020, is positive and neutral.

![](https://github.com/kyleehum/kyleehum.github.io/blob/main/images/vaccineSAplot.png)
