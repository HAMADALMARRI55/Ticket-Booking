class Payment:
    def __init__(self, payment_id, payment_method):
        """
        Initialize a payment with basic details.
        :param payment_id: Unique identifier for the payment (str).
        :param payment_method: Chosen payment method (str).
        """
        self.payment_id = payment_id
        self.payment_method = payment_method.lower()
        self.status = "Pending"

    def process_payment(self, amount):
        """
        Process the payment based on the payment method.
        :param amount: The amount to be paid (float).
        :return: True if payment is successful, False otherwise.
        """
        print(f"Processing payment of {amount} DHS using {self.payment_method.capitalize()}...")
        if self.payment_method == "net banking":
            return self._process_net_banking(amount)
        elif self.payment_method == "credit card":
            return self._process_credit_card(amount)
        elif self.payment_method == "digital wallet":
            return self._process_digital_wallet(amount)
        elif self.payment_method == "cash":
            return self._process_cash(amount)
        elif self.payment_method == "coupon":
            return self._process_coupon(amount)
        else:
            print("Invalid payment method!")
            return False

    def _process_net_banking(self, amount):
        """
        Simulate processing payment via net banking.
        """
        # Simulate a successful net banking payment
        print("Net banking transaction successful.")
        self.status = "Success"
        return True

    def _process_credit_card(self, amount):
        """
        Simulate processing payment via credit card.
        """
        # Simulate credit card validation and processing
        print("Credit card transaction approved.")
        self.status = "Success"
        return True

    def _process_digital_wallet(self, amount):
        """
        Simulate processing payment via a digital wallet.
        """
        # Simulate a successful digital wallet transaction
        print("Digital wallet payment successful.")
        self.status = "Success"
        return True

    def _process_cash(self, amount):
        """
        Simulate cash payment.
        """
        # Cash payments are always assumed successful
        print("Cash payment accepted.")
        self.status = "Success"
        return True

    def _process_coupon(self, amount):
        """
        Simulate processing payment via coupon.
        :return: True if coupon is valid and covers the amount, False otherwise.
        """
        # Simulate coupon validation
        coupon_value = 100  # Example fixed coupon value
        if amount <= coupon_value:
            print("Coupon applied successfully.")
            self.status = "Success"
            return True
        else:
            print(f"Coupon value insufficient. Remaining amount: {amount - coupon_value} DHS.")
            self.status = "Failed"
            return False

    def __str__(self):
        """
        String representation of the payment.
        :return: Payment details as a string.
        """
        return f"Payment ID: {self.payment_id}, Method: {self.payment_method.capitalize()}, Status: {self.status}"
