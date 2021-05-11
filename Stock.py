# pip install yfinance
# pip install matplotlib
import yfinance as yf
import matplotlib.pyplot as plt


def get_stock_data(ticker_list, start_date, end_date, interval):
    data = yf.download(
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
    # Plot the close prices
    data.Close.plot()
    plt.show()


get_stock_data(ticker_list='MSFT', start_date="2021-04-10",
               end_date="2021-04-10", interval='5m')
