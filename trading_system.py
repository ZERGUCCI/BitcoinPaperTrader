import numpy as np
from datetime import datetime


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

file_path = "HistoricalBTCdata.txt"
historical_data = load_historical_data(file_path)

