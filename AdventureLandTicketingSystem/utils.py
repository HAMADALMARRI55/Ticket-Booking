import re
import uuid
from datetime import date, datetime

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
    
    @staticmethod
    def validate_date(input_date):
        """
        Validate the format of a date and ensure it is not in the past.
        :param input_date: The input date as a string in YYYY-MM-DD format.
        :return: True if valid and not in the past, False otherwise.
        """
        try:
            date_obj = datetime.strptime(input_date, "%Y-%m-%d")
            today = datetime.now().date()
            return date_obj.date() >= today
        except ValueError:
            return False    
