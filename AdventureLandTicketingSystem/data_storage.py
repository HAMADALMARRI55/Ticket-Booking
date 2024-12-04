import pickle
import os

class DataStorage:
    """
    A utility class for saving and loading data using Pickle.

    Provides static methods to save data to files and load data from files, handling directory creation if needed.
    """
    @staticmethod
    def save_to_file(data, filename):
        """
        Save data to a binary file using Pickle. Creates the folder if it doesn't exist.

        Args:
            data: The data object to be saved.
            filename (str): The path to the file where data should be saved.

        Returns:
            None
        """
        # Ensure the directory exists
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Save the data
        with open(filename, 'wb') as file:
            pickle.dump(data, file)
            print(f"Data saved to {filename}.")

    @staticmethod
    def load_from_file(filename):
        """
        Load data from a binary file using Pickle.

        Args:
            filename (str): The path to the file from which data should be loaded.

        Returns:
            Any: The data object loaded from the file, or an empty dictionary if the file does not exist.
        """
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                data = pickle.load(file)
                print(f"Data loaded from {filename}.")
                return data
        else:
            print(f"{filename} not found. Returning empty data.")
            return {}
