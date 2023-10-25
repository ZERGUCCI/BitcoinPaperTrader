import numpy as np
from datetime import datetime
from datetime import timedelta
import pytz

class Wallet:
    def __init__(self, initial_cash):
        self.cash = initial_cash
        self.stock = 0
        self.transactions = []

    def buy(self, timestamp, price, number):

        # Input validation
        if np.isnan(price) or price <= 0:
            print(f"Price: {price} is invalid")
            return False # Invalid price input
        
        if self.transactions and timestamp <= self.transactions[-1]['timestamp']:
            print(f"Cannot go back in time")
            return False  # Cannot buy before previous transaction.
        
        if price * number > self.cash:
            print(f"Not enough cash to buy that number")
            return False  # Not enough cash to buy

        if number <= 0:
            print(f"Cannot buy 0 or negative amount")
            return False # Invalid number input
        
        # Update Wallet
        self.cash -= price * number
        self.stock += number
        transaction = {
            'type': 'buy', 
            'price': price, 
            'number': number, 
            'timestamp': timestamp
        }
        self.transactions.append(transaction)

        # Logging
        print(transaction)
        return True

    def sell(self, timestamp, price, number):

        # Input Validation
        if np.isnan(price) or price <= 0:
            print(f"Price: {price} is invalid")
            return False # Invalid price input
        
        if self.transactions and timestamp <= self.transactions[-1]['timestamp']:
            print(f"Cannot go back in time")
            return False  # Cannot buy before previous transaction.
        
        if number > self.stock:
            print(f"Not enough stock to sell")
            return False  # Not enough stock to sell
        
        if number <= 0:
            print(f"Cannot buy 0 or negative amount")
            return False # Invalid number input

        # Update Wallet
        self.stock -= number
        self.cash += price * number
        transaction = {
            'type': 'sell', 
            'price': price, 
            'number': number, 
            'timestamp': timestamp
        }
        self.transactions.append(transaction)

        # Logging
        print(transaction)
        return True


def load_historical_data(file_path):
    try:
        print("Loading Sim Data...")
        with open(file_path) as f:
            lines = f.read().split("\n")
            lines = [line.split(",") for line in lines if line]  # Avoid empty strings
            data_points = [[int(line[0]), float(line[1])] for line in lines]

        print(f"{len(data_points)} minutes of data loaded")
        return data_points

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def test_data_loading(data):
    print(f"{len(data)} number of entries loaded")
    print(data[0])

def get_user_input():
    wallet = input("Please enter the starting size (in dollars) of the wallet you would like to simulate: ")
    start_date = input("Enter the start date (mm-dd-yyyy): ")
    end_date = input("Enter the end date (mm-dd-yyyy): ")
    data_time_interval = input("Enter the time interval in seconds (minimum 60): ")
    return wallet, start_date, end_date, data_time_interval


def user_settings(wallet, start_date, end_date, data_time_interval, historical_data):
    first_timestamp = historical_data[0][0]
    last_timestamp = historical_data[-1][0]

    # Convert inputs and validate them
    try:
        wallet = float(wallet)
        if wallet <= 0:
            raise ValueError("Wallet size must be positive.")

        # Time conversion stuff
        utc_tz = pytz.utc
        start_date_obj = datetime.strptime(start_date, '%m-%d-%Y')
        end_date_obj = datetime.strptime(end_date, '%m-%d-%Y')
        start_date_obj = utc_tz.localize(start_date_obj)
        end_date_obj = utc_tz.localize(end_date_obj)
        start_timestamp = int(start_date_obj.timestamp()) + 60
        end_timestamp = int(end_date_obj.timestamp()) + 60

        data_time_interval = int(data_time_interval)
        if data_time_interval < 60:
            raise ValueError("Time interval must be at least 60 seconds.")

        if not (first_timestamp <= start_timestamp <= last_timestamp) or not (first_timestamp <= end_timestamp <= last_timestamp):
            raise ValueError("Start date and end date must be within the range of historical data.")

        if start_timestamp > end_timestamp:
            raise ValueError("End date must be after the start date.")

    except ValueError as e:
        print(f"Invalid input: {e}")
        return None, None

    # Filter data between time range then adjust to data interval
    filtered_data = [data_point for data_point in historical_data if start_timestamp <= data_point[0] <= end_timestamp]

    adjusted_data = []
    current_time = start_timestamp

    for i in range(0, len(filtered_data), data_time_interval // 60):
        if filtered_data[i][0] >= current_time:
            adjusted_data.append(filtered_data[i])
            current_time += data_time_interval

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