class User:
    def __init__(self, user_id, name, email, password):
        """
        Initialize a User object with basic details.
        
        :param user_id: Unique ID for the user (str)
        :param name: Name of the user (str)
        :param email: Email address of the user (str)
        :param password: Password for the user's account (str)
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.purchase_history = []  # Stores a list of purchased tickets

    def create_account(self, name, email, password):
        """
        Create a new user account. This function would normally
        interact with a database, but here we'll just update the instance.
        
        :param name: Name of the user (str)
        :param email: Email address of the user (str)
        :param password: Password for the account (str)
        """
        self.name = name
        self.email = email
        self.password = password
        print(f"Account created for {self.name} with email {self.email}.")

    def login(self, email, password):
        """
        Simulate a login process.
        
        :param email: Entered email address (str)
        :param password: Entered password (str)
        :return: Boolean indicating success or failure
        """
        if self.email == email and self.password == password:
            print("Login successful!")
            return True
        else:
            print("Invalid email or password. Please try again.")
            return False

    def view_tickets(self):
        """
        Display the user's ticket purchase history.
        """
        if not self.purchase_history:
            print("No tickets purchased yet.")
        else:
            print("Your purchased tickets:")
            for ticket in self.purchase_history:
                print(f" - {ticket}")

    def purchase_ticket(self, ticket):
        """
        Add a ticket to the user's purchase history.
        
        :param ticket: Ticket object (or placeholder for now)
        """
        self.purchase_history.append(ticket)
        print(f"Ticket '{ticket}' added to your purchase history.")
