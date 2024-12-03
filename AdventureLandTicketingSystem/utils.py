import re
import uuid
from datetime import date

class Utils:
    @staticmethod
    def validate_email(email):
        """
        Validate if the email is in a correct format.
        :param email: The email address to validate (str).
        :return: True if valid, False otherwise (bool).
        """
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return re.match(pattern, email) is not None

    @staticmethod
    def generate_unique_id():
        """
        Generate a unique identifier for objects.
        :return: A unique identifier string.
        """
        return str(uuid.uuid4())

    @staticmethod
    def calculate_discounted_price(base_price, discount_percentage):
        """
        Calculate the price after applying a discount.
        :param base_price: Original price (float).
        :param discount_percentage: Discount as a fraction (float, e.g., 0.10 for 10%).
        :return: Discounted price (float).
        """
        if not (0 <= discount_percentage <= 1):
            raise ValueError("Discount percentage must be between 0 and 1.")
        return base_price * (1 - discount_percentage)

    @staticmethod
    def validate_positive_number(value):
        """
        Validate that the given value is a positive number.
        :param value: The value to validate (float or int).
        :return: True if valid, False otherwise (bool).
        """
        return isinstance(value, (int, float)) and value > 0

    @staticmethod
    def get_today_date():
        """
        Get today's date in a string format (YYYY-MM-DD).
        :return: Today's date as a string.
        """
        return date.today().isoformat()
