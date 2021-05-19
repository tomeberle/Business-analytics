import pandas as pd

from Stock import get_stock_data_2min_56days
from Twitter_CEO import get_CEOs_twitter_posts
from Twitter_Company import get_company_twitter_posts

# Load list of companies
companies = pd.read_csv("assets/twitter_accounts.csv")
symbols = companies["symbol"].tolist()

# Fetch stock data
stock_prices = get_stock_data_2min_56days(symbols)

# Fetch Twitter CEO Posts
CEO_tweets = get_CEOs_twitter_posts(companies)
# Add Stock Price Movement in new column

print(CEO_tweets)


# Fetch Twitter Company Posts
company_tweets = get_company_twitter_posts(companies)
print(company_tweets)

# Add Stock Price Movement in new column


# Statistical tests Company Posts & CEO Posts
