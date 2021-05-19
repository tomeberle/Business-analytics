import pandas as pd

from Stock import get_stock_data_2min_56days
from Twitter_CEO import get_CEOs_twitter_posts
from Twitter_Company import get_company_twitter_posts

# Load list of companies
companies = pd.read_csv("assets/twitter_accounts.csv")
symbols = companies["symbol"].tolist()

# Fetch stock data
get_stock_data_2min_56days(symbols)

# Fetch Twitter Company Posts
get_company_twitter_posts(companies)

# Add Stock Price Movement in new column

# Fetch Twitter CEO Posts
get_CEOs_twitter_posts(companies)

# Add Stock Price Movement in new column

# Statistical tests Company Posts & CEO Posts
