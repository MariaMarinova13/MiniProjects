import requests
import json
import mysql.connector
from datetime import datetime


url = "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT"
time_url = "https://api.binance.com/api/v3/time"

mydb = mysql.connector.connect(
    host="localhost",
    user="username",
    password="mypassword",
    database="BTC_data")

cursor = mydb.cursor()
cursor.execute("CREATE TABLE orderbook_BTC (Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, TradeDate CHAR(20), BidPrice FLOAT(7,2), BidQty FLOAT(6,5), AskPrice FLOAT(7,2), AskQty FLOAT(6,5), CONSTRAINT unique_rows UNIQUE(TradeDate, BidPrice, BidQty, AskPrice, AskQty));")
print("Table created")

def get_binance_data():
    time_response = requests.get(time_url)
    epoch_time = time_response.json()
    timestamp = datetime.fromtimestamp(epoch_time['serverTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    response = requests.get(url)
    btc_data = response.json()

    sql = "INSERT INTO orderbook_BTC (TradeDate, BidPrice, BidQty, AskPrice, AskQty) VALUES (%s, %s, %s, %s, %s)"
    val = (timestamp, btc_data['bidPrice'], btc_data['bidQty'], btc_data['askPrice'], btc_data['askQty'])
    try:
        cursor.execute(sql, val)
    except Exception:
        print("duplicate_keys")
    mydb.commit()
    print(timestamp, btc_data['bidPrice'], btc_data['bidQty'], btc_data['askPrice'], btc_data['askQty'])

while True:
    get_binance_data()



