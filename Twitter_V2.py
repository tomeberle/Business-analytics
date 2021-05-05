import csv
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime

# Creating list to append tweet data to
tweets_list1 = []
# Using TwitterSearchScraper to scrape data and append tweets to list
for tweet in sntwitter.TwitterSearchScraper('from:cnbc since:2021-05-01').get_items():
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.username])
for tweet in sntwitter.TwitterSearchScraper('from:WSJmarkets since:2021-05-01').get_items():
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.username])

# Creating a dataframe from the tweets list above & cleaning
tweets_df1 = pd.DataFrame(tweets_list1, columns=[
                          'Datetime', 'Tweet Id', 'Text', 'Username'])
tweets_df1['Text'] = tweets_df1['Text'].str.lower()
# getting rid of everything except letters (a-z)
tweets_df1['Text'] = tweets_df1['Text'].replace(
    r'[^a-z ]', '', regex=True).replace("'", '')
tweets_df1['Text'] = tweets_df1['Text'].apply(lambda x: ' '.join(
    [y for y in x.split() if 'http' not in y]))  # getting rid of the links
tweets_df1['Datetime'] = tweets_df1['Datetime'] + \
    datetime.timedelta(hours=+2)  # fixing time to Paris time
# splitting datetime into date and time
tweets_df1['Date'] = [d.date() for d in tweets_df1['Datetime']]
tweets_df1['Time'] = [d.time() for d in tweets_df1['Datetime']]
del tweets_df1['Datetime']
del tweets_df1['Tweet Id']
column_names = ['Username', 'Date', 'Time', 'Text']  # reordering columns
tweets_df1 = tweets_df1.reindex(columns=column_names)

# Sentiment Analysis

SENTIMENT_CSV = "assets/word_sentiment.csv"
NEGATIVE_WORDS = ["not", "dont", "doesnt", "no", "arent", "isnt"]


def word_sentiment(word):
    with open(SENTIMENT_CSV, 'rt', encoding='utf-8') as senti_data:
        sentiment = csv.reader(senti_data)
        for data_row in sentiment:
            if data_row[0] == word.lower():
                sentiment_val = data_row[1]
                return sentiment_val
        return 0


def sentiment(sentence):
    sentiment = 0
    words_list = sentence.split()
    for word in words_list:
        previous_index = words_list.index(word) - 1
        if words_list[previous_index] in NEGATIVE_WORDS:
            sentiment = sentiment + -1 * int(word_sentiment(word))
        else:
            sentiment = sentiment + int(word_sentiment(word))
    return sentiment


tweets_df1['Sentiment'] = tweets_df1['Text'].apply(sentiment)

# Export as CSV
tweets_df1.to_csv(
    r'output\twitter_sentiment.csv', encoding='utf-8-sig')
