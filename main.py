import pandas as pd

from Stock import get_stock_data_2min_56days


# Load list of companies
companies = pd.read_csv("assets/twitter_accounts.csv")
companies = companies["symbol"].tolist()

# Fetch stock data
get_stock_data_2min_56days(companies)
