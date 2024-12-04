from user import User

class Admin(User):
    """
    Represents an admin user in the Adventure Land Theme Park Ticketing System.

    Inherits from the User class and provides additional functionalities
    specific to administrators, such as managing discounts and viewing sales reports.
    """
    def __init__(self, user_id, name, email, password):
        """
        Initialize an Admin object.

        Args:
            user_id (str): Unique identifier for the admin.
            name (str): Name of the admin.
            email (str): Email address of the admin.
            password (str): Password for admin authentication.
        """
        super().__init__(user_id, name, email, password)

    def manage_discounts(self, ticket, discount):
        """
        Set or modify discounts for tickets.

        Args:
            ticket (Ticket): The ticket object whose discount is to be updated.
            discount (float): The new discount value (e.g., 0.15 for 15% discount).

        Returns:
            None
        """
        ticket.discount = discount
        print(f"Discount for ticket '{ticket.ticket_type}' set to {discount * 100}%.")

    def view_sales(self, sales_reports):
        """
        Display sales reports.

        Args:
            sales_reports (list or dict): Collection of sales reports to be displayed.

        Returns:
            None
        """
        print("Sales Reports:")
        for report in sales_reports:
            print(report)
