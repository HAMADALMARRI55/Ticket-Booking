import pickle
import os

class DataStorage:
    @staticmethod
    def save_to_file(data, filename):
        """
        Save data to a binary file using Pickle. Create the folder if it doesn't exist.
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
        """
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                data = pickle.load(file)
                print(f"Data loaded from {filename}.")
                return data
        else:
            print(f"{filename} not found. Returning empty data.")
            return {}
