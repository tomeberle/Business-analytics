import pandas as pd

from Stock import get_stock_data_2min_56days
from Twitter_CEO import get_CEOs_twitter_posts
from Twitter_Company import get_company_twitter_posts
from Analysis import find_stock_movement
from statistical_tests import contingency_table_company, contingency_table_ceo, run_chisquared_company, run_chisquared_ceo

# Parameters
TIME_BEFORE_TWEET = 2  # in minutes
TIME_AFTER_TWEET = 2  # in minutes
SENSITIVITY = 0.0004  # threshold for significant price movement

# Load list of companies
companies = pd.read_csv("assets/twitter_accounts.csv")
symbols = companies["symbol"].tolist()

# Fetch stock data
stock_prices = get_stock_data_2min_56days(symbols)

# Fetch Twitter CEO Posts
CEO_tweets = get_CEOs_twitter_posts(companies)
# Fetch Twitter Company Posts
company_tweets = get_company_twitter_posts(companies)

# Add Stock Price Movement in new column
CEO_tweets['Movement'] = CEO_tweets.apply(lambda x: find_stock_movement(
    x['Symbol'], x['Datetime'], time_after_tweet=TIME_AFTER_TWEET, time_before_tweet=TIME_BEFORE_TWEET, sensitivity=SENSITIVITY, df=stock_prices), axis=1)
company_tweets['Movement'] = company_tweets.apply(lambda x: find_stock_movement(
    x['Symbol'], x['Datetime'], time_after_tweet=TIME_AFTER_TWEET, time_before_tweet=TIME_BEFORE_TWEET, sensitivity=SENSITIVITY, df=stock_prices), axis=1)

CEO_tweets.to_csv("output/twitter_sentiment_ceos.csv")
company_tweets.to_csv("output/twitter_sentiment_companies.csv")

print(CEO_tweets)
print(company_tweets)


# Statistical tests Company Posts & CEO Posts
sentiment_company = pd.read_csv("output/twitter_sentiment_companies.csv")
sentiment_ceo = pd.read_csv("output/twitter_sentiment_ceos.csv")

contingency_table_company(sentiment_company)
contingency_table_ceo(sentiment_ceo)
run_chisquared_company(sentiment_company)
run_chisquared_ceo(sentiment_ceo)


# Cramer's V companies
import numpy as np
data = np.array([[21,57,24], [270,500,259], [280,740,320]])
chi2 = 11.11
n = np.sum(data)
minDim = min(data.shape)-1
V = np.sqrt((chi2/n) / minDim)
print(V)

# Cramer's V CEOs
import numpy as np
data = np.array([[21,57,24], [270,500,259], [280,740,320]])
chi2 = 11.11
n = np.sum(data)
minDim = min(data.shape)-1
V = np.sqrt((chi2/n) / minDim)
print(V)