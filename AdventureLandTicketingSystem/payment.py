class Payment:
    def __init__(self, payment_id, payment_method):
        """
        Initialize a Payment object.
        """
        self.payment_id = payment_id
        self.payment_method = payment_method

    def process_payment(self, amount):
        """
        Simulate payment processing.
        """
        print(f"Processing payment of {amount} using {self.payment_method}.")
        # Simulate payment success
        return True
