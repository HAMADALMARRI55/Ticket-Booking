class User:
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

    def view_purchase_history(self):
        """
        Display purchased tickets.
        """
        if not self.purchase_history:
            print("No tickets purchased yet.")
        else:
            print("Purchase History:")
            for ticket in self.purchase_history:
                print(ticket)

    def purchase_ticket(self, ticket):
        """
        Add a ticket to purchase history.
        """
        self.purchase_history.append(ticket)
        print(f"Ticket '{ticket}' purchased successfully.")
