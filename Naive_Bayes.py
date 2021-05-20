import random
import nltk
import pandas as pd
from datetime import datetime, timedelta
import json


def train_nb_classifier(df):
    """ This will train the classifier using the word sentiment feature set"""
    featureset = gen_featureset(df)

    # Shuffle the corpus to avoid chronology
    random.shuffle(featureset)

    num_ts = int(len(featureset)*0.8)
    # the first 80% as training set, the latter 20% as test set
    training_set, test_set = featureset[:num_ts], featureset[num_ts:]
    # training_set = featureset[:num_ts]
    # test_set = featureset[num_ts:]

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    classifier.show_most_informative_features(20)
    print("Starting accuracy test...")
    b = nltk.classify.accuracy(classifier, training_set)
    print("The accuracy of the training:", b)
    acc = nltk.classify.accuracy(classifier, test_set)
    print("The accuracy of the model:", acc)

    return classifier


def gen_featureset(df):
    """ This function creates a feature set from the given dataframe"""
    # Load stock data
    stock_data = pd.read_csv("output/historical.csv", parse_dates=["Date"])
    # Loop through each tweets
    featureset = list()
    print('Generating features... (up to 1min)')
    for i in range(len(df.dropna())):
        # Locating relevant information
        ticker = df.loc[i, "Symbol"]
        sentiment = df.loc[i, "Sentiment"]
        stock_mouvement = df.loc[i, "Movement"]
        tweet_date = df.loc[i, "Datetime"]
        tweet_text = df.loc[i, "Text"]

        # Generating features
        volatility = feature_stockprice_volatility(
            ticker, tweet_date, time_before=120, df=stock_data)

        # If no volatility information, skip row
        if volatility is not None:

            feature_label = list()

            feature = {'ticker': ticker, 'sentiment': sentiment,
                       'volatility': volatility}
            feature_label.append(feature)
            feature_label.append(stock_mouvement)

            featureset.append(feature_label)
    return featureset


def feature_stockprice_volatility(ticker, date, time_before, df):
    """
    Functions that finds the stock price volatility for a certain stock, at a certain point in time.
    Input: ticker (e.g. "MSFT"), date (format "2021-03-26 14:20:00-04:00"), time_before (in minutes), df (historical.csv)
    Output: returns volatility (standard deviation) as a number
    """

    # Working on dates to create the interval to check
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S%z")
    date_minus_delta = date - timedelta(minutes=time_before)

    # Finding tickers that matches the requested one
    df = df.loc[df['Ticker'] == ticker]

    # Extract stock price within interval
    df = df[(df['Date'] > date_minus_delta)
            & (df['Date'] < date)]

    # If no stock data, returns N/A
    if df.empty:
        return None

    # Compute standard deviation
    sd = df.std(axis=0, skipna=True)
    sd = sd.loc['Adj Close']
    # Compute mean
    x = df.mean(axis=0, skipna=True, numeric_only=True)
    x = x.loc['Adj Close']
    # Compute normalised standard deviation, rounded up
    nsd = round(sd/x, 2)
    return nsd


# ticker = 'MSFT'
# date = '2021-04-05 09:38:00-04:00'
# df = pd.read_csv("output/historical.csv", parse_dates=["Date"])
# volatility = feature_stockprice_volatility(ticker, date, time_before=20, df=df)

df_ceos = pd.read_csv("output/twitter_sentiment_ceos.csv")
df_companies = pd.read_csv("output/twitter_sentiment_companies.csv")

nb_classifier = train_nb_classifier(df_ceos)
nb_classifier = train_nb_classifier(df_companies)
