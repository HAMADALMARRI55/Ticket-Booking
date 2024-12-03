class Ticket:
    def __init__(self, ticket_id, ticket_type, price, validity):
        """
        Initialize a Ticket object.
        """
        self.ticket_id = ticket_id
        self.ticket_type = ticket_type
        self.price = price
        self.validity = validity
        self.discount = 0.0  # Default no discount

    def apply_discount(self):
        """
        Apply a discount to the ticket price.
        """
        discounted_price = self.price * (1 - self.discount)
        return discounted_price

    def __str__(self):
        """
        String representation of the ticket.
        """
        return f"{self.ticket_type} - Price: {self.price}, Validity: {self.validity}"
