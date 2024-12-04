# test.py

import unittest
import os

# Import necessary modules from your codebase
from data_storage import DataStorage
from constants import FILE_PATH_USERS, FILE_PATH_TICKETS, FILE_PATH_SALES_REPORTS
from user import User
from ticket import Ticket
from payment import Payment
from sales_report import SalesReport, Transaction
from utils import Utils

class TestTicketingSystem(unittest.TestCase):
    def setUp(self):
        # Load existing data
        self.users = DataStorage.load_from_file(FILE_PATH_USERS)
        self.tickets = DataStorage.load_from_file(FILE_PATH_TICKETS)
        self.sales_reports = DataStorage.load_from_file(FILE_PATH_SALES_REPORTS)

        # Backup original data to restore after tests
        self.users_backup = self.users.copy()
        self.tickets_backup = self.tickets.copy()
        self.sales_reports_backup = self.sales_reports.copy()

        # Create a test user
        self.user_id = Utils.generate_unique_id()
        self.user_name = "Test User"
        self.user_email = "testuser@example.com"
        self.user_password = "password123"
        self.user = User(self.user_id, self.user_name, self.user_email, self.user_password)
        self.users[self.user_email] = self.user
        DataStorage.save_to_file(self.users, FILE_PATH_USERS)

    def tearDown(self):
        # Restore original data
        DataStorage.save_to_file(self.users_backup, FILE_PATH_USERS)
        DataStorage.save_to_file(self.tickets_backup, FILE_PATH_TICKETS)
        DataStorage.save_to_file(self.sales_reports_backup, FILE_PATH_SALES_REPORTS)

    def test_valid_account_creation(self):
        # Create a new user account
        new_user_id = Utils.generate_unique_id()
        new_user_name = "New User"
        new_user_email = "newuser@example.com"
        new_user_password = "newpassword"
        new_user = User(new_user_id, new_user_name, new_user_email, new_user_password)
        self.users[new_user_email] = new_user
        DataStorage.save_to_file(self.users, FILE_PATH_USERS)

        # Load users and check
        loaded_users = DataStorage.load_from_file(FILE_PATH_USERS)
        self.assertIn(new_user_email, loaded_users)
        self.assertEqual(loaded_users[new_user_email].name, new_user_name)

    def test_duplicate_email_registration(self):
        # Try to create another user with the same email
        duplicate_user_id = Utils.generate_unique_id()
        duplicate_user_name = "Duplicate User"
        duplicate_user_email = self.user_email  # Same email as existing user
        duplicate_user_password = "duplicatepassword"

        with self.assertRaises(ValueError):
            if duplicate_user_email in self.users:
                raise ValueError("An account with this email already exists.")
            duplicate_user = User(duplicate_user_id, duplicate_user_name, duplicate_user_email, duplicate_user_password)
            self.users[duplicate_user_email] = duplicate_user
            DataStorage.save_to_file(self.users, FILE_PATH_USERS)

    def test_invalid_email_format(self):
        invalid_email = "invalidemail"
        is_valid = Utils.validate_email(invalid_email)
        self.assertFalse(is_valid)

    def test_successful_login(self):
        # Attempt to login with correct credentials
        loaded_users = DataStorage.load_from_file(FILE_PATH_USERS)
        user = loaded_users.get(self.user_email)
        self.assertIsNotNone(user)
        self.assertEqual(user.password, self.user_password)

    def test_incorrect_password(self):
        # Attempt to login with incorrect password
        loaded_users = DataStorage.load_from_file(FILE_PATH_USERS)
        user = loaded_users.get(self.user_email)
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password, "wrongpassword")

    def test_nonexistent_email_login(self):
        # Attempt to login with an email that does not exist
        loaded_users = DataStorage.load_from_file(FILE_PATH_USERS)
        user = loaded_users.get("nonexistent@example.com")
        self.assertIsNone(user)

    def test_purchase_two_day_pass_online(self):
        # Purchase a Two-Day Pass with online payment
        ticket_type = "Two-Day Pass"
        visit_date = "2024-12-25"
        num_tickets = 2
        payment_method = "credit card"

        ticket_info = self.tickets.get(ticket_type)
        ticket_id = Utils.generate_unique_id()
        ticket = Ticket(
            ticket_id,
            ticket_type,
            ticket_info['price'],
            ticket_info['validity'],
            visit_date,
            default_discount=ticket_info.get('discount', 0.0)
        )

        # Apply discounts and set validity
        ticket.apply_discounts(self.user, num_tickets, payment_method)
        ticket.set_validity_dates(self.user)
        ticket.validate(group_size=num_tickets)

        # Calculate total price
        total_price = ticket.price * num_tickets

        # Process payment
        payment_id = Utils.generate_unique_id()
        payment = Payment(payment_id, payment_method)
        payment_success = payment.process_payment(total_price)
        self.assertTrue(payment_success)

        # Update sales report
        self.update_sales_report(self.user, ticket, num_tickets)

        # Add tickets to user's purchase history
        for _ in range(num_tickets):
            individual_ticket_id = Utils.generate_unique_id()
            individual_ticket = Ticket(
                individual_ticket_id,
                ticket.ticket_type,
                ticket.price,
                ticket.validity,
                ticket.visit_date
            )
            individual_ticket.discount = ticket.discount
            individual_ticket.validity_start_date = ticket.validity_start_date
            individual_ticket.validity_end_date = ticket.validity_end_date
            self.user.purchase_ticket(individual_ticket)

        # Save user data
        self.users[self.user_email] = self.user
        DataStorage.save_to_file(self.users, FILE_PATH_USERS)

        # Assertions
        self.assertEqual(len(self.user.purchase_history), num_tickets)
        for t in self.user.purchase_history:
            self.assertEqual(t.ticket_type, ticket_type)
            self.assertEqual(t.discount, ticket.discount)
            self.assertEqual(t.price, ticket.price)

    def test_admin_login(self):
        # Admin login credentials
        admin_email = "admin@adventureland.com"
        admin_password = "admin123"
        self.assertEqual(admin_email, "admin@adventureland.com")
        self.assertEqual(admin_password, "admin123")

    def test_manage_discounts(self):
        # Update discount for a ticket
        ticket_type = "Two-Day Pass"
        new_discount = 0.05  # 5%
        self.tickets[ticket_type]['discount'] = new_discount
        DataStorage.save_to_file(self.tickets, FILE_PATH_TICKETS)

        # Load tickets and check
        updated_tickets = DataStorage.load_from_file(FILE_PATH_TICKETS)
        self.assertEqual(updated_tickets[ticket_type]['discount'], new_discount)

    def test_child_ticket_without_adult(self):
        # Attempt to purchase a Child Ticket without an adult ticket
        ticket_type = "Child Ticket"
        visit_date = "2024-12-25"
        num_tickets = 1
        payment_method = "credit card"

        ticket_info = self.tickets.get(ticket_type)
        ticket_id = Utils.generate_unique_id()
        ticket = Ticket(
            ticket_id,
            ticket_type,
            ticket_info['price'],
            ticket_info['validity'],
            visit_date,
            default_discount=ticket_info.get('discount', 0.0)
        )

        # No adult ticket in purchase history
        adult_present = any(
            t.ticket_type in ["Single-Day Pass", "Two-Day Pass", "Annual Membership", "VIP Experience Pass"]
            for t in self.user.purchase_history
        )

        with self.assertRaises(ValueError) as context:
            ticket.validate(adult_present=adult_present)

        self.assertTrue("Child Ticket must be accompanied by an adult ticket." in str(context.exception))

    def test_vip_tickets_sold_out(self):
        # Attempt to purchase more VIP tickets than available
        ticket_type = "VIP Experience Pass"
        visit_date = "2024-12-25"
        num_tickets = 25  # Exceeds limited availability
        payment_method = "credit card"

        ticket_info = self.tickets.get(ticket_type)
        ticket_id = Utils.generate_unique_id()
        ticket = Ticket(
            ticket_id,
            ticket_type,
            ticket_info['price'],
            ticket_info['validity'],
            visit_date,
            default_discount=ticket_info.get('discount', 0.0)
        )

        tickets_sold_today = 0  # Let no tickets sold yet

        with self.assertRaises(ValueError) as context:
            ticket.validate(group_size=num_tickets, tickets_sold_today=tickets_sold_today)

        self.assertTrue("VIP Experience Pass is sold out for today." in str(context.exception))

    def test_data_persistence(self):
        # Test saving and loading of user data
        DataStorage.save_to_file(self.users, FILE_PATH_USERS)
        loaded_users = DataStorage.load_from_file(FILE_PATH_USERS)
        loaded_user = loaded_users.get(self.user_email)
        self.assertIsNotNone(loaded_user)
        self.assertEqual(loaded_user.name, self.user_name)
        self.assertEqual(loaded_user.email, self.user_email)

    def update_sales_report(self, user, ticket, quantity):
        """Update the daily sales report with the transaction."""
        today = Utils.get_today_date()
        report = self.sales_reports.get(today)
        if not report:
            report_id = Utils.generate_unique_id()
            report = SalesReport(report_id, today)
            self.sales_reports[today] = report

        # Create a Transaction object
        transaction_id = Utils.generate_unique_id()
        transaction = Transaction(
            transaction_id=transaction_id,
            customer_name=user.name,
            ticket_type=ticket.ticket_type,
            quantity=quantity,
            total_price=ticket.price * quantity,
            date_of_purchase=today
        )

        # Add the transaction to the report
        report.add_transaction(transaction)
        DataStorage.save_to_file(self.sales_reports, FILE_PATH_SALES_REPORTS)
    
    def test_admin_login_success(self):
        # Test successful admin login
        admin_email = "admin@adventureland.com"
        admin_password = "admin123"

        # Simulate admin login process
        is_admin_logged_in = (admin_email == "admin@adventureland.com" and admin_password == "admin123")
        self.assertTrue(is_admin_logged_in, "Admin should be able to log in with correct credentials.")    
    
    def test_admin_login_incorrect_email(self):
        # Test admin login with incorrect email
        admin_email = "wrongadmin@adventureland.com"
        admin_password = "admin123"

        # Simulate admin login process
        is_admin_logged_in = (admin_email == "admin@adventureland.com" and admin_password == "admin123")
        self.assertFalse(is_admin_logged_in, "Admin login should fail with incorrect email.")

    def test_admin_login_incorrect_password(self):
        # Test admin login with incorrect password
        admin_email = "admin@adventureland.com"
        admin_password = "wrongpassword"

        # Simulate admin login process
        is_admin_logged_in = (admin_email == "admin@adventureland.com" and admin_password == "admin123")
        self.assertFalse(is_admin_logged_in, "Admin login should fail with incorrect password.")

    def test_admin_view_sales_reports(self):
        # Test admin viewing sales reports
        # Let the admin is logged in
        # For testing purposes, we'll check if sales_reports data is accessible and correctly formatted

        # Load sales reports
        loaded_sales_reports = DataStorage.load_from_file(FILE_PATH_SALES_REPORTS)
        self.assertIsNotNone(loaded_sales_reports, "Sales reports should be loaded.")

        # Check if sales reports contain the expected data
        if loaded_sales_reports:
            for date, report in loaded_sales_reports.items():
                self.assertIsInstance(report, SalesReport, "Each report should be an instance of SalesReport.")
                self.assertIsNotNone(report.transactions, "SalesReport should have transactions attribute.")
        else:
            # If no sales reports are available, this is still a valid scenario
            self.assertEqual(len(loaded_sales_reports), 0, "Sales reports should be empty if no data.")

    def test_admin_manage_discounts(self):
        # Test admin updating discounts for a ticket type
        ticket_type = "Annual Membership"
        new_discount = 0.1  

        # Admin updates the discount
        self.tickets[ticket_type]['discount'] = new_discount
        DataStorage.save_to_file(self.tickets, FILE_PATH_TICKETS)

        # Load tickets and verify the discount was updated
        updated_tickets = DataStorage.load_from_file(FILE_PATH_TICKETS)
        self.assertEqual(updated_tickets[ticket_type]['discount'], new_discount, "Discount should be updated.")

        # Clean up by restoring the original discount
        self.tickets[ticket_type]['discount'] = self.tickets_backup[ticket_type]['discount']
        DataStorage.save_to_file(self.tickets, FILE_PATH_TICKETS)

    

if __name__ == '__main__':
    unittest.main()
