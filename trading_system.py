import numpy as np
from datetime import datetime
from datetime import timedelta
import pytz


def load_historical_data(file_path):
    """
    Load and parse historical trading data from a file.

    :param file_path: Path to the historical data file.
    :return: List of parsed data points.
    """
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

def user_settings(historical_data):

    first_timestamp = historical_data[0][0]
    last_timestamp = historical_data[-1][0]

    earliest_date = datetime.utcfromtimestamp(first_timestamp).strftime('%m-%d-%Y')
    latest_date = datetime.utcfromtimestamp(last_timestamp).strftime('%m-%d-%Y')

    while True:
        try:
            # Read in user inputs
            wallet = float(input("Please enter the starting size (in dollars) of the wallet you would like to simulate: "))
            if wallet <= 0:
                print("Wallet size must be positive. Please try again.")
                continue

            print(f"The earliest start date available is {earliest_date}.")
            start_date = input("Enter the start date (mm-dd-yyyy): ")

            print(f"The latest end date available is {latest_date}.")
            end_date = input("Enter the end date (mm-dd-yyyy): ")

            data_time_interval = int(input("Enter the time interval in seconds (minimum 60): "))

            # Time conversion stuff
            utc_tz = pytz.utc
            start_date_obj = datetime.strptime(start_date, '%m-%d-%Y')
            end_date_obj = datetime.strptime(end_date, '%m-%d-%Y')
            start_date_obj = utc_tz.localize(start_date_obj)
            end_date_obj = utc_tz.localize(end_date_obj)
            start_timestamp = int(start_date_obj.timestamp()) + 60
            end_timestamp = int(end_date_obj.timestamp()) + 60

            # Input validation
            if data_time_interval < 60:
                print("Time interval must be at least 60 seconds. Please try again.")
                continue

            if not (first_timestamp <= start_timestamp <= last_timestamp) or not (first_timestamp <= end_timestamp <= last_timestamp):
                print("Start date and end date must be within the range of historical data. Please try again.")
                continue

            if start_timestamp > end_timestamp:
                print("End date must be after the start date. Please try again.")
                continue

            break  
        except ValueError:
            print("Invalid input. Please ensure you enter the correct values and formats.")


    # Filter data between time range then adjust to data interval
    filtered_data = [data_point for data_point in historical_data if start_timestamp <= data_point[0] <= end_timestamp]

    adjusted_data = []
    current_time = start_timestamp

    for i in range(0, len(filtered_data), data_time_interval // 60):
        if filtered_data[i][0] >= current_time:
            adjusted_data.append(filtered_data[i])
            current_time += data_time_interval

    return wallet, adjusted_data

# Main execution starts here
file_path = "HistoricalBTCdata.txt"
historical_data = load_historical_data(file_path)
wallet, adjusted_historical_data = user_settings(historical_data)
