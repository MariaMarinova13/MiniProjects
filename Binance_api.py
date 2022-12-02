import requests
import json
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import mplfinance as mpf


url = "https://api.binance.com/api/v3/klines"


def get_binance_data(symbol, interval, starttime, endtime):

    #Hourly data for BTC extracted from Binance
    startTime = str(int(starttime.timestamp() * 1000))
    endTime = str(int(endtime.timestamp() * 1000))
    limit = '1000'
    req_params = {"symbol": symbol, "interval": interval, "startTime": startTime, "endTime": endTime, "limit": limit}
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    global df
    df = pd.DataFrame(json.loads(requests.get(url, params=req_params).text))
    df = df.iloc[:, 0:9]
    df.columns = ['datetime','open', 'high', 'low', 'close', 'volume', 'Close time', 'Quote asset volume', 'Number of trades']
    df['datetime'] = pd.to_datetime(df['datetime']/1000, unit='s')
    df['Open_Time'] = [d.time() for d in df['datetime']]
    df['datetime'] = [d.date() for d in df['datetime']]
    df.rename(columns={'datetime':'Open_Date'}, inplace = True)
    col = df.pop("Open_Time")
    df.insert(1, col.name, col)
    df['Open_Time'] = df['Open_Time'].astype(pd.StringDtype())
    df['Close time'] = pd.to_datetime(df['Close time']/1000, unit='s')
    df['Close_Time'] = [d.time() for d in df['Close time']]
    df['Close time'] = [d.date() for d in df['Close time']]
    df.rename(columns={'Close time': 'Close_Date'}, inplace=True)
    col = df.pop("Close_Time")
    df.insert(8, col.name, col)
    df[df.columns[2:7]] = df[df.columns[2:7]].astype('float')
    df['Quote asset volume'] = df['Quote asset volume'].astype('float32')
    df = df.round(2)
    print(df)

get_binance_data('BTCUSDT', '1h', dt.datetime(2022, 10, 1), dt.datetime(2022, 11, 1))


def get_daily_data(symbol, interval, starttime, endtime):

    #Daily data extracted from Binance
    startTime = str(int(starttime.timestamp() * 1000))
    endTime = str(int(endtime.timestamp() * 1000))
    limit = '1000'
    req_params = {"symbol": symbol, "interval": interval, "startTime": startTime, "endTime": endTime, "limit": limit}
    global df2
    df2 = pd.DataFrame(json.loads(requests.get(url, params=req_params).text))
    df2 = df2.iloc[:, 0:6]
    df2.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
    df2['datetime'] = pd.to_datetime(df2['datetime'] / 1000, unit='s')
    df2[df2.columns[1:6]] = df2[df2.columns[1:6]].astype('float')
    df2 = df2.round(2)

    df2['price change in pct'] = ((df2['close'] - df2['open']) / df2['open']) * 100
    df2['day of week'] = df2['datetime'].dt.day_name()
    col = df2.pop('day of week')
    df2.insert(1, col.name, col)
    df2['day of week'] = pd.Categorical(df2['day of week'], categories=
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
    print(df2)
get_daily_data('BTCUSDT', '1d', dt.datetime(2022, 1, 1), dt.datetime(2022, 11, 16))

def data_anlysis():
    #Grouping the data for the last month by hour
    by_hour = df.groupby(['Open_Time'], as_index=False).mean(numeric_only=True)
    by_hour = by_hour.round(2)

    # In which part of the day is the highest trade volume.
    # The graphics show high correlation between the trade volume and the number of trades.
    # They also show the busiest time of the day is between 13:00 and 15:00.
    plt.subplot(1, 2, 1)
    plt.plot(by_hour['Open_Time'], by_hour['volume'])
    plt.xticks(by_hour['Open_Time'], rotation='vertical', size=8)
    plt.xlabel("Time")
    plt.ylabel("Trade Volume")
    plt.title("Average Trade volumes during the day for October")
    plt.subplot(1, 2, 2)
    plt.plot(by_hour['Open_Time'], by_hour['Number of trades'])
    plt.xticks(by_hour['Open_Time'], rotation='vertical', size=8)
    plt.xlabel("Time")
    plt.ylabel("Number of trades")
    plt.title("Average Number of trades during the day for October")
    plt.show()

    # Price movements day by day for October
    by_day = df.groupby(['Open_Date'], as_index=False).mean(numeric_only=True)
    by_day.index = pd.DatetimeIndex(by_day['Open_Date'])
    mpf.plot(by_day, type='line', volume=True, style='yahoo', title='Bitcoin data October 2022')
    plt.show()
    # We see the price of BTC for October was between 19100 USD and 20800 USD
    # When the price was in an uptrend around OCt 22-Oct 25, the volume quantities were also in an uptrend.
    print(by_day)

    #A graphic of the price movements for the year
    #Checking if there is a high correlation between the trading volume and the price
    #The Graphic shows the volumes are at the highest levels after the last big price drop.
    df2.index = pd.DatetimeIndex(df2['datetime'])
    mpf.plot(df2, type='candle', volume=True, style='yahoo', title='Bitcoin data 2022')
    plt.show()
    #Calculating the pct change between opening and closing price for each day.
    y = df2['price change in pct']
    color = (y > 0).apply(lambda x: 'g' if x else 'r')
    plt.bar(df2['datetime'], y, color=color)
    plt.xlabel("Time")
    plt.ylabel("Price Change in %")
    plt.title("BTC Price Change in %")
    plt.show()
    # We see that the biggest change in price for a day is around 15%.

    # Grouping the data by day of the week in order to see if the volumes during the year were higher on a particular day of the week.
    by_week_day = df2.groupby(['day of week'], as_index=False).mean(numeric_only=True)
    print(by_week_day)
    by_week_day['day of week'] = pd.Categorical(by_week_day['day of week'], categories=
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'], ordered=True)
    plt.bar(by_week_day['day of week'], by_week_day['volume'])
    plt.xlabel("Day of the week")
    plt.ylabel("Volume")
    plt.title("BTC Price Change in %")
    plt.show()
    # As expected the volumes drop significantly during the weekend.

data_anlysis()