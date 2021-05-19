from cleanco import prepare_terms, basename
import csv
import pandas as pd
from datetime import datetime, timedelta
import time

content = []


def load_csv(filename, subfolder):
    """ Loads CSV easily
    Input: filename, subfolder. E.g. assets/nasdaq.csv -->  filename='assets', subfolder='nasdaq.csv' 
    Output: data
    """
    with open(subfolder + '/' + filename + '.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def find_companies(content):
    """ Identifies stock market companies in scrapped content. 
    Input: [[counter, date, _time, title, author, likes, comments], [...]]
    Output: identical list with new 'company' column. 
    Notes: removes the 1 line of the list (header)
    """
    nasdaq = load_csv(filename='nasdaq-listed_clean', subfolder='assets')
    test_string = "This text is about a company called credit suisse company and , of couse, is it working"

    # Removing headers
    content.pop(0)

    # TODO: for loop to check if company is in: title, content, etc.
    for row in content:
        # Input: [counter,date,_time,title,author,likes,comments,url,content]
        tickers = ''
        title = row[3]
        content = row[8]

        for company in nasdaq:
            # Looking company name
            match_name = title.find(company[1])
            if match_name != -1:
                print(row[0] + '- Found company in title: ' + str(company))
            # Looking ticker
            match_symbol = title.find('$' + company[0])
            if match_symbol != -1:
                print(row[0] + '- Found ticker in title: ' + str(company))

    # TODO: Better matching accuracy
    # TODO: create new column with tickers


def find_stock_movement(ticker, date, time_before_tweet, time_after_tweet, sensitivity, df):
    """
    Functions that finds the stock price movement for a given ticker and time.
    Input: ticker (e.g. "MSFT"), date (format "2021-03-26 14:20:00-04:00"), time_before_tweet, time_after_tweet (in minutes)
    Output: returns +1, -1, 0 or None (corresponding to upward move, downward move, no siginificant move, no stock data)
    """
    print('Called with:' + str([ticker, date]))

    # Working on dates to create the interval to check
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S%z")
    date_plus_delta = date + timedelta(minutes=time_after_tweet)
    date_minus_delta = date - timedelta(minutes=time_before_tweet)

    # Finding tickers that matches the requested one
    df = df.loc[df['Ticker'] == ticker]

    # Extract stock price within interval
    df = df[(df['Date'] > date_minus_delta)
            & (df['Date'] < date_plus_delta)]

    # If no stock data, returns N/A
    if df.empty:
        print('DataFrame is empty!')
        return None

    # Filter for first and last in interval
    df = df.iloc[[0, -1]]
    print(df)
    price_start = df['Close'].values[0]
    price_close = df['Close'].values[1]

    # Assess price movement
    delta = (price_close - price_start) / price_start
    print('Delta : ' + str(delta))
    print('Start price was ' + str(price_start) +
          ' Close price was ' + str(price_close) + '.'+'Ticker: '+ticker+'. Date: ' + str(date) + '. Delta: ' + str(delta))
    if (abs(delta) >= sensitivity):
        # Significant movement
        if delta > 0:
            return 1
        if delta < 0:
            return -1
        else:
            return 0
    else:
        # Not significant
        return 0


# a = find_stock_movement(ticker, date, interval_minutes=20, sensitivity=0.01)
# print('a :', a)
