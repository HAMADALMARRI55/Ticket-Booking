from datetime import datetime

class Transaction:
    def __init__(self, transaction_id, customer_name, ticket_type, quantity, total_price, date_of_purchase):
        """
        Initialize a Transaction object.
        """
        self.transaction_id = transaction_id
        self.customer_name = customer_name
        self.ticket_type = ticket_type
        self.quantity = quantity
        self.total_price = total_price
        self.date_of_purchase = date_of_purchase

    def __str__(self):
        """
        String representation of the transaction.
        """
        return (f"Transaction ID: {self.transaction_id}\n"
                f"Customer Name: {self.customer_name}\n"
                f"Ticket Type: {self.ticket_type}\n"
                f"Quantity: {self.quantity}\n"
                f"Total Price: {self.total_price:.2f} DHS\n"
                f"Date of Purchase: {self.date_of_purchase}\n")

class SalesReport: 
    def __init__(self, report_id, date):
        """
        Initialize a sales report.
        """
        self.report_id = report_id
        self.date = date
        self.transactions = []

    def add_transaction(self, transaction):
        """
        Add a transaction to the sales report.
        """
        self.transactions.append(transaction)

    def __str__(self):
        """
        String representation of the sales report.
        """
        report_str = f"Sales Report - Date: {self.date}\n"
        report_str += f"Total Transactions: {len(self.transactions)}\n"
        report_str += "Transactions Details:\n"
        for transaction in self.transactions:
            report_str += str(transaction) + "\n"
        return report_str

    @staticmethod
    def generate_report_id(date):
        """
        Generate a unique report ID based on the date.
        """
        return f"REPORT-{date.replace('-', '')}-{int(datetime.now().timestamp())}"
