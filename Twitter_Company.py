import csv
import snscrape.modules.twitter as sntwitter
import pandas as pd
import os.path


def get_company_twitter_posts(account_df1):
    # Check if file exist
    if os.path.isfile("output/twitter_sentiment_companies.csv"):
        print("File already exist - skipping company data extraction.")
        return pd.read_csv("output/twitter_sentiment_companies.csv")

    print("Company tweets extraction...")
    # Creating list to append tweet data to
    tweets_list1 = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    account_list = account_df1["twitter_account_company"].values.tolist()
    symbol_list = account_df1["symbol"].values.tolist()

    for index, account in enumerate(account_list):
        symbol = symbol_list[index]
        for tweet in sntwitter.TwitterSearchScraper('from:' + account + ' since:2021-04-05 until:2021-05-18').get_items():
            print([tweet.date, tweet.id, tweet.content, tweet.username, symbol])
            tweets_list1.append(
                [tweet.date, tweet.id, tweet.content, tweet.username, symbol])

    # Creating a dataframe from the tweets list above
    tweets_df1 = pd.DataFrame(tweets_list1, columns=[
        'Datetime', 'Tweet Id', 'Text', 'Username', 'Symbol'])

    # Dropping replies
    tweets_df1['First'] = tweets_df1['Text'].astype(str).str[0]
    tweets_df1.drop(tweets_df1[tweets_df1['First'] == '@'].index, inplace=True)
    del tweets_df1['First']

    tweets_df1['Text'] = tweets_df1['Text'].str.lower()

    # getting rid of everything except letters (a-z)
    tweets_df1['Text'] = tweets_df1['Text'].apply(lambda x: ' '.join(
        [y for y in x.split() if 'http' not in y]))  # getting rid of the links
    tweets_df1['Text'] = tweets_df1['Text'].apply(lambda x: ' '.join(
        [y for y in x.split() if '#' not in y]))  # getting rid of the hashtags

    tweets_df1['Text'] = tweets_df1['Text'].replace("'", '', regex=True)
    tweets_df1['Text'] = tweets_df1['Text'].replace("’", '', regex=True)
    tweets_df1['Text'] = tweets_df1['Text'].replace(
        r'[^a-z ]', ' ', regex=True)

    tweets_df1['Text'] = tweets_df1['Text'].str.replace(' +', ' ')

    del tweets_df1['Tweet Id']
    column_names = ['Username', 'Datetime',
                    'Text', 'Symbol']  # reordering columns
    tweets_df1 = tweets_df1.reindex(columns=column_names)
    print(tweets_df1)
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
    tweets_df1.to_csv('output/twitter_sentiment_companies.csv',
                      encoding='utf-8-sig')
    return tweets_df1
