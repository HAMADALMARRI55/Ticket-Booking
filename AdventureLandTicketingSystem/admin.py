from user import User

class Admin(User):
    def __init__(self, user_id, name, email, password):
        """
        Initialize an Admin object.
        """
        super().__init__(user_id, name, email, password)

    def manage_discounts(self, ticket, discount):
        """
        Set or modify discounts for tickets.
        """
        ticket.discount = discount
        print(f"Discount for ticket '{ticket.ticket_type}' set to {discount * 100}%.")

    def view_sales(self, sales_reports):
        """
        Display sales reports.
        """
        print("Sales Reports:")
        for report in sales_reports:
            print(report)
