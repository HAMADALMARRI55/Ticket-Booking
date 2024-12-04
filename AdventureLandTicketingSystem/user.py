class User:
    """
    Represents a user in the Adventure Land Theme Park Ticketing System.

    Attributes:
        user_id (str): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        password (str): Password for user authentication.
        purchase_history (list): List of tickets purchased by the user.
    """
    def __init__(self, user_id, name, email, password):
        """
        Initialize a User object with basic details.
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.purchase_history = []  # Stores purchased ticket details

    def create_account(self, name, email, password):
        """
        Simulate account creation.
        """
        self.name = name
        self.email = email
        self.password = password
        print(f"Account created for {self.name} with email {self.email}.")

    def login(self, email, password):
        """
        Simulate a login process.
        """
        return self.email == email and self.password == password

    def load_purchase_history(self, history):
        updated_history = []
        for ticket in history:
            if not hasattr(ticket, "visit_date"):
                ticket.visit_date = "Unknown"
            updated_history.append(ticket)
        self.purchase_history = updated_history

    def view_purchase_history(self):
        if not self.purchase_history:
            print("No tickets purchased yet.")
            return
        print("\nPurchase History:")
        for ticket in self.purchase_history:
            visit_date = getattr(ticket, "visit_date", "Unknown")
            print(f"{ticket.ticket_type} - Price: {ticket.price} DHS, "
                f"Validity: {ticket.validity}, Visit Date: {visit_date}")

    def purchase_ticket(self, ticket):
        """
        Add a ticket to purchase history.
        """
        self.purchase_history.append(ticket)
        print(f"Ticket '{ticket}' purchased successfully.")
