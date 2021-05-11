# pip install yfinance
# pip install matplotlib
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import time


def get_stock_data(ticker_list, start_date, end_date, interval):
    """ data = yf.download(
        tickers=ticker_list,
        start=start_date,
        end=end_date,
        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        #  period="1d",
        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval=interval)
        """
    # data = yf.download('AAPL MC.PA', '2021-01-01', '2021-08-01', interval="1h")
    data = yf.download(ticker_list, start_date, end_date, interval=interval)
    # Plot the close prices
    print(data)
    data.Close.plot()
    plt.show()


def get_stock_data_2min_56days(ticker_list):
    """
    Get's stock data every 2min for the last 56 days. Stops on same time yesterday (e.g. today() - 1 day).
    Input: ticker_list=['AAPL', 'MSFT']
    Output: CSV 'assets/historical.csv' with [Date,Ticker,Adj Close,Close,High,Low,Open,Volume]
    """

    dates = pd.date_range(end=datetime.today().strftime(
        '%Y-%m-%d'), periods=8, freq='7D')
    print(dates)

    i = 0
    dataframe = pd.DataFrame([])
    for date in dates:
        print(date)
        if i < 7:
            data = yf.download(
                ticker_list, dates[i], dates[i+1], group_by='Ticker', interval="2m")
            # print(data)
            data = data.stack(level=0).rename_axis(
                ['Date', 'Ticker']).reset_index(level=1)
            dataframe = dataframe.append(data)
            print(dataframe)
            time.sleep(2)

        i += 1
    dataframe.to_csv("assets/historical.csv")
    # end =
    #data = yf.download(ticker_list, start_date, end_date, interval="1m")
    # Plot the close prices
    # print(data)


# Example usage
# get_stock_data(ticker_list="AAPL MC.PA", start_date="2021-03-01", end_date="2021-04-06", interval="15m")
get_stock_data_2min_56days(ticker_list=['AAPL', 'MSFT'])
