from cleanco import prepare_terms, basename
import csv
import pandas as pd
from datetime import datetime
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


def find_stock_movement(ticker, datetime):
    df = pd.read_csv("output/historical.csv")
    datetime = datetime.strptime(datetime, "%Y-%m-%d %H:%M:%S%z")
    print(datetime.tzinfo)

    # Find tickers that match
    # Check if time is within time

    #df = df.assign(Timestamp=pd.Series(datetime.timestamp(df.Date)))
    # print(df)
    #content = load_csv(filename='reddit_output', subfolder='output')
    # find_companies(content)


ticker = "WSJmarkets"
datetime = "2021-03-26 14:20:00-04:00"


find_stock_movement(ticker, datetime)
