from datetime import datetime, timedelta

class Ticket:
    def __init__(self, ticket_id, ticket_type, price, validity, visit_date, default_discount=0.0):
        """
        Initialize a ticket with basic details.
        :param ticket_id: Unique identifier for the ticket (str).
        :param ticket_type: Type of the ticket (e.g., Single-Day Pass) (str).
        :param price: Base price of the ticket (float).
        :param validity: Validity duration of the ticket (str).
        :param visit_date: Date of visit in YYYY-MM-DD format (str).
        :param default_discount: Default discount set by admin (float).
        """
        self.ticket_id = ticket_id
        self.ticket_type = ticket_type
        self.price = price
        self.base_price = price  # Keep a record of the original price
        self.validity = validity
        self.visit_date = visit_date
        self.discount = 0.0  # Total accumulated discount
        self.default_discount = default_discount  # Discount from tickets data (set by admin)
        self.validity_start_date = None
        self.validity_end_date = None
        self.limited_availability = 20  # Default for VIP tickets per day

    def apply_discounts(self, user, num_tickets, payment_method):
        """Apply discounts based on ticket type and conditions."""
        # Apply default discount from tickets data
        if self.default_discount > 0:
            self.apply_discount(self.default_discount)

        # For Two-Day Pass, 10% discount for online purchases
        if self.ticket_type == "Two-Day Pass" and payment_method in ["net banking", "credit card", "digital wallet"]:
            self.apply_discount(0.10)

        # For Group Ticket (10+), 20% discount for groups of 20 or more
        if self.ticket_type == "Group Ticket (10+)" and num_tickets >= 20:
            self.apply_discount(0.20)

        # For Annual Membership renewal, 15% discount
        if self.ticket_type == "Annual Membership":
            previous_membership = any(
                t.ticket_type == "Annual Membership" for t in user.purchase_history
            )
            if previous_membership:
                self.apply_discount(0.15)

    def set_validity_dates(self, user):
        """Set the validity start and end dates based on ticket type."""
        start_date = datetime.strptime(self.visit_date, "%Y-%m-%d").date()
        if self.ticket_type == "Single-Day Pass":
            self.validity_start_date = start_date
            self.validity_end_date = start_date
        elif self.ticket_type == "Two-Day Pass":
            self.validity_start_date = start_date
            self.validity_end_date = start_date + timedelta(days=1)
        elif self.ticket_type == "Annual Membership":
            previous_memberships = [t for t in user.purchase_history if t.ticket_type == "Annual Membership"]
            if previous_memberships:
                last_membership = max(previous_memberships, key=lambda t: t.validity_end_date)
                self.validity_start_date = last_membership.validity_end_date + timedelta(days=1)
                self.validity_end_date = self.validity_start_date + timedelta(days=365)
            else:
                self.validity_start_date = start_date
                self.validity_end_date = start_date + timedelta(days=365)
        elif self.ticket_type == "Child Ticket":
            self.validity_start_date = start_date
            self.validity_end_date = start_date
        elif self.ticket_type == "VIP Experience Pass":
            self.validity_start_date = start_date
            self.validity_end_date = start_date
        elif self.ticket_type == "Group Ticket (10+)":
            self.validity_start_date = start_date
            self.validity_end_date = start_date

    def apply_discount(self, discount_percentage):
        """Apply a discount to the ticket price."""
        if not (0 <= discount_percentage <= 1):
            raise ValueError("Discount percentage must be between 0 and 1.")
        self.discount += discount_percentage  # Accumulate discounts
        discounted_price = self.base_price * (1 - self.discount)
        self.price = round(discounted_price, 2)  # Update price with discount applied

    def validate(self, group_size=1, adult_present=False, tickets_sold_today=0):
        """Validate ticket-specific rules."""
        if self.ticket_type == "Child Ticket" and not adult_present:
            raise ValueError("Child Ticket must be accompanied by an adult ticket.")
        if self.ticket_type == "Group Ticket (10+)" and group_size < 10:
            raise ValueError("Group Ticket requires a minimum of 10 tickets.")
        if self.ticket_type == "VIP Experience Pass" and tickets_sold_today + group_size > self.limited_availability:
            raise ValueError("VIP Experience Pass is sold out for today.")

    def __str__(self):
        discount_str = f" (Discount Applied: {self.discount * 100}%)" if self.discount > 0 else ""
        validity_str = f", Validity: From {self.validity_start_date} to {self.validity_end_date}"
        return f"{self.ticket_type} - Price: {self.price} DHS{validity_str}, Visit Date: {self.visit_date}{discount_str}"
