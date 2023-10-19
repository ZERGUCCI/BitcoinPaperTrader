import sys
import unittest
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from trading_system import load_historical_data

class TestLoadHistoricalData(unittest.TestCase):
    def test_load_valid_data(self):
        result = load_historical_data('test_data/valid_data.txt')
        self.assertEqual(len(result), 50)  # assuming the file contains 50 data points

    def test_file_not_found(self):
        result = load_historical_data('non_existent_file.txt')
        self.assertEqual(result, [], "Expected an empty list when trying to load a non-existent file.")

    def test_empty_file(self):
        result = load_historical_data('test_data/empty_file.txt')
        self.assertEqual(len(result), 0)

    def test_first_data_point(self):
        test_file_path = 'test_data/valid_data.txt'
        data_points = load_historical_data(test_file_path)
        self.assertTrue(data_points, "Failed to load data points from file.")
        first_data_point = data_points[0]
        expected_first_data_point = [1483228860, 966.34]
        self.assertEqual(first_data_point, expected_first_data_point, "The first data point does not match the expected value.")

    def test_second_data_point(self):
        test_file_path = 'test_data/valid_data.txt'
        data_points = load_historical_data(test_file_path)
        self.assertTrue(data_points, "Failed to load data points from file.")
        second_data_point = data_points[1]
        expected_second_data_point = [1483228920, 966.30547933]
        self.assertEqual(second_data_point, expected_second_data_point, "The second data point does not match the expected value.")

    def test_last_data_point(self):
        test_file_path = 'test_data/valid_data.txt'
        data_points = load_historical_data(test_file_path)
        self.assertTrue(data_points, "Failed to load data points from file.")
        last_data_point = data_points[len(data_points) - 1]
        expected_last_data_point = [1483231800, 966.97]
        self.assertEqual(last_data_point, expected_last_data_point, "The last data point does not match the expected value.")

    def test_non_numeric_data(self):
        result = load_historical_data('test_data/non_numeric_data.txt')
        self.assertIsInstance(result, list)

    def test_incomplete_data_lines(self):
        result = load_historical_data('test_data/incomplete_data.txt')
        self.assertIsInstance(result, list)

    def test_huge_file(self):
        result = load_historical_data('HistoricalBTCdata.txt')
        self.assertIsInstance(result, list)
    
    def test_last_huge_file(self):
        test_file_path = 'HistoricalBTCdata.txt'
        data_points = load_historical_data(test_file_path)
        self.assertTrue(data_points, "Failed to load data points from file.")
        last_data_point = data_points[len(data_points) - 1]
        expected_last_data_point = [1609372800, 28909.166061]
        self.assertEqual(last_data_point, expected_last_data_point, "The last data point does not match the expected value.")

    def test_file_with_extra_spaces(self):
        result = load_historical_data('test_data/extra_spaces.txt')
        self.assertIsInstance(result, list)

    def test_very_old_timestamps(self):
        result = load_historical_data('test_data/old_timestamps.txt')
        self.assertIsInstance(result, list)

    def test_future_timestamps(self):
        result = load_historical_data('test_data/future_timestamps.txt')
        self.assertIsInstance(result, list)
    
    def test_return_type_time(self):
        result = load_historical_data('test_data/valid_data.txt')
        self.assertIsInstance(result[0][0], int)
    
    def test_return_type_price(self):
        result = load_historical_data('test_data/valid_data.txt')
        self.assertIsInstance(result[0][1], float)
    
  
def main():
    suite = unittest.TestSuite()

    test_cases = unittest.TestLoader().loadTestsFromTestCase(TestLoadHistoricalData)
    suite.addTests(test_cases)

    result = unittest.TextTestRunner().run(suite)

    if result.wasSuccessful():
        sys.exit(0)  # All tests passed, exit with code 0
    else:
        sys.exit(1)  # Some tests failed, exit with code 1

if __name__ == "__main__":
    main()