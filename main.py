import pandas as pd

from Stock import get_stock_data_2min_56days


# Load list of companies
companies = pd.read_csv("assets/twitter_accounts.csv")
symbols = companies["symbol"].tolist()

# Fetch stock data
get_stock_data_2min_56days(symbols)

# Fetch Twitter Company Posts
# Add Stock Price Movement in new column

# Fetch Twitter CEO Posts
# Add Stock Price Movement in new column

# Statistical tests Company Posts & CEO Posts
