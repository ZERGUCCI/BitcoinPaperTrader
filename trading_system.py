import numpy as np
from datetime import datetime
from datetime import timedelta
import pytz

class TechnicalIndicators:

    # Method to create heiken ashi price candles
    @staticmethod
    def heikin_ashi(data_point, previous_candle):
        open_ = data_point['open']
        high = data_point['high']
        low = data_point['low']
        close = data_point['close']

        if previous_candle is None:
            return { 'open': open_, 'high': high, 'low': low, 'close': close }

        new_candle = {}
        new_candle['open'] = (previous_candle['open'] + previous_candle['close']) / 2
        new_candle['high'] = max(high, new_candle['open'], close)
        new_candle['low'] = min(low, new_candle['open'], close)
        new_candle['close'] = (open_ + high + low + close) / 4

        return new_candle


class Wallet:
    def __init__(self, initial_cash):
        self.cash = initial_cash
        self.stock = 0
        self.transactions = []

    def buy(self, timestamp, price, number):
        if np.isnan(price) or price <= 0:
            print(f"Price: {price} is invalid")
            return False
        
        if self.transactions and timestamp <= self.transactions[-1]['timestamp']:
            print(f"Cannot go back in time")
            return False 
        
        if price * number > self.cash:
            print(f"Not enough cash to buy that number")
            return False 

        if number <= 0:
            print(f"Cannot buy 0 or negative amount")
            return False 

        self.cash -= price * number
        self.stock += number
        transaction = {
            'type': 'buy',
            'price': price,
            'number': number,
            'timestamp': timestamp
        }
        self.transactions.append(transaction)

        print(transaction)
        return True

    def sell(self, timestamp, price, number):
        if np.isnan(price) or price <= 0:
            print(f"Price: {price} is invalid")
            return False 

        if self.transactions and timestamp <= self.transactions[-1]['timestamp']:
            print(f"Cannot go back in time")
            return False 

        if number > self.stock:
            print(f"Not enough stock to sell")
            return False 

        if number <= 0:
            print(f"Cannot sell 0 or negative amount")
            return False 

        self.stock -= number
        self.cash += price * number
        transaction = {
            'type': 'sell',
            'price': price,
            'number': number,
            'timestamp': timestamp
        }
        self.transactions.append(transaction)

        print(transaction)
        return True


def load_historical_data(file_path):
    try:
        print("Loading Sim Data...")
        with open(file_path) as f:
            lines = f.read().split("\n")
            lines = [line.split(",") for line in lines if line]  
            data_points = [[int(line[0]), float(line[1])] for line in lines]

        print(f"{len(data_points)} minutes of data loaded")
        return data_points

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def minute_to_ohlc(data, interval):
    ohlc_data = []

    for i in range(0, len(data), interval):
        time_period = data[i:i + interval]
        timestamps, prices = zip(*time_period)
        
        ohlc = {}
        ohlc['timestamp'] = timestamps[0]
        ohlc['open'] = prices[0]
        ohlc['high'] = max(prices)
        ohlc['low'] = min(prices)
        ohlc['close'] = prices[-1]

        ohlc_data.append(ohlc)
    
    return ohlc_data


def get_user_input():
    wallet = input("Please enter the starting size (in dollars) of the wallet you would like to simulate: ")
    start_date = input("Enter the start date (mm-dd-yyyy): ")
    end_date = input("Enter the end date (mm-dd-yyyy): ")
    data_time_interval = input("Enter the time interval in minutes: ")
    return wallet, start_date, end_date, data_time_interval


def user_settings(wallet, start_date, end_date, data_time_interval, historical_data):
    first_timestamp = historical_data[0][0]
    last_timestamp = historical_data[-1][0]

    try:
        wallet = float(wallet)
        if wallet <= 0:
            raise ValueError("Wallet size must be positive.")

        utc_tz = pytz.utc
        start_date_obj = datetime.strptime(start_date, '%m-%d-%Y')
        end_date_obj = datetime.strptime(end_date, '%m-%d-%Y')
        start_date_obj = utc_tz.localize(start_date_obj)
        end_date_obj = utc_tz.localize(end_date_obj)
        start_timestamp = int(start_date_obj.timestamp()) + 60
        end_timestamp = int(end_date_obj.timestamp()) + 60

        data_time_interval = int(data_time_interval)

        if data_time_interval < 1:
            raise ValueError("Time interval must be at least 1 minute.")

        if not (first_timestamp <= start_timestamp <= last_timestamp) or not (first_timestamp <= end_timestamp <= last_timestamp):
            raise ValueError("Start date and end date must be within the range of historical data.")

        if start_timestamp > end_timestamp:
            raise ValueError("End date must be after the start date.")

    except ValueError as e:
        print(f"Invalid input: {e}")
        return None, None

    filtered_data = [data_point for data_point in historical_data if start_timestamp <= data_point[0] <= end_timestamp]
    adjusted_data = minute_to_ohlc(filtered_data, data_time_interval)

    return wallet, adjusted_data


if __name__ == "__main__":
    file_path = "HistoricalBTCdata.txt"
    historical_data = load_historical_data(file_path)

    while True:
        wallet, start_date, end_date, data_time_interval = get_user_input()

        wallet, adjusted_historical_data = user_settings(wallet, start_date, end_date, data_time_interval, historical_data)

        if wallet is not None and adjusted_historical_data is not None:
            break
        else:
            print("Invalid input received. Please try again.")

    userWallet = Wallet(wallet)