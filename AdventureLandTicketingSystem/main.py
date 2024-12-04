from data_storage import DataStorage
from constants import FILE_PATH_USERS, FILE_PATH_TICKETS, FILE_PATH_SALES_REPORTS
from user import User
from admin import Admin
from ticket import Ticket
from payment import Payment
from utils import Utils
import sys
from sales_report import SalesReport, Transaction



# Load data
users = DataStorage.load_from_file(FILE_PATH_USERS)
tickets = DataStorage.load_from_file(FILE_PATH_TICKETS)
sales_reports = DataStorage.load_from_file(FILE_PATH_SALES_REPORTS)

def initialize_tickets():
    """Initialize default tickets if tickets.pkl is missing."""
    if not tickets:
        print("Initializing ticket data...")
        tickets_data = {
            "Single-Day Pass": {"price": 275, "validity": "1 Day", "discount": 0.0},
            "Two-Day Pass": {"price": 480, "validity": "2 Days", "discount": 0.0},
            "Annual Membership": {"price": 1840, "validity": "1 Year", "discount": 0.0},
            "Child Ticket": {"price": 185, "validity": "1 Day", "discount": 0.0},
            "Group Ticket (10+)": {"price": 220, "validity": "1 Day", "discount": 0.0},
            "VIP Experience Pass": {"price": 550, "validity": "1 Day", "discount": 0.0},
        }
        DataStorage.save_to_file(tickets_data, FILE_PATH_TICKETS)
        print("Ticket data initialized.")

def main_menu():
    initialize_tickets()
    while True:
        print("\nMain Menu:")
        print("1. Create User Account")
        print("2. User Login")
        print("3. Admin Login")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                create_user_account()
            elif choice == 2:
                user_login()
            elif choice == 3:
                admin_login()
            elif choice == 4:
                print("Exiting... Saving data.")
                DataStorage.save_to_file(users, FILE_PATH_USERS)
                DataStorage.save_to_file(tickets, FILE_PATH_TICKETS)
                DataStorage.save_to_file(sales_reports, FILE_PATH_SALES_REPORTS)
                sys.exit()
            else:
                print("Invalid choice! Please enter a valid option.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def create_user_account():
    try:
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        if not Utils.validate_email(email):
            raise ValueError("Invalid email format!")

        user_id = Utils.generate_unique_id()
        new_user = User(user_id, name, email, password)
        users[email] = new_user
        DataStorage.save_to_file(users, FILE_PATH_USERS)
        print("Account created successfully!")
    except Exception as e:
        print(f"Error: {e}")

def create_user_account():
    try:
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        if not Utils.validate_email(email):
            raise ValueError("Invalid email format!")

        user_id = Utils.generate_unique_id()
        new_user = User(user_id, name, email, password)
        users[email] = new_user
        DataStorage.save_to_file(users, FILE_PATH_USERS)
        print("Account created successfully!")
    except Exception as e:
        print(f"Error: {e}")

def user_login():
    try:
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        user = users.get(email)
        if user and user.password == password:
            user.load_purchase_history(user.purchase_history)
            print(f"Welcome, {user.name}!")
            user_menu(user)
        else:
            print("Invalid email or password!")
    except Exception as e:
        print(f"Error: {e}")

def user_menu(user):
    while True:
        print("\nUser Menu:")
        print("1. View Purchase History")
        print("2. Purchase Ticket")
        print("3. Logout")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                user.view_purchase_history()
            elif choice == 2:
                purchase_ticket(user)
            elif choice == 3:
                print("Logging out...")
                break
            else:
                print("Invalid choice! Please enter a valid option.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def purchase_ticket(user):
    try:
        print("Available Tickets:")
        for ticket_type, details in tickets.items():
            print(f"{ticket_type}: {details['price']} DHS, Validity: {details['validity']}")

        ticket_type_input = input("Enter the ticket type: ")
        ticket_type = ticket_type_input.strip()
        if ticket_type not in tickets:
            raise ValueError("Invalid ticket type!")

        ticket_info = tickets[ticket_type]

        visit_date = input("Enter the visit date (YYYY-MM-DD): ")
        if not Utils.validate_date(visit_date):
            raise ValueError("Invalid or past date!")

        num_tickets = int(input("Enter the number of tickets: "))
        if num_tickets <= 0:
            raise ValueError("The number of tickets must be greater than 0.")

        adult_present = True  # Default assumption

        # For Child Ticket, ensure an adult ticket is purchased
        if ticket_type == "Child Ticket":
            adult_present = any(
                t.ticket_type in ["Single-Day Pass", "Two-Day Pass", "Annual Membership", "VIP Experience Pass"]
                for t in user.purchase_history
            )
            if not adult_present:
                print("An adult ticket must be purchased with a Child Ticket.")
                # Ask if the user wants to purchase an adult ticket
                purchase_adult = input("Would you like to purchase an adult ticket as well? (yes/no): ").lower()
                if purchase_adult == "yes":
                    # Proceed to purchase an adult ticket
                    print("Please purchase an adult ticket first.")
                    return
                else:
                    raise ValueError("Cannot purchase a Child Ticket without an accompanying adult ticket.")

        # Get payment method before applying discounts
        print("Payment Methods:")
        print("1. Net Banking")
        print("2. Credit Card")
        print("3. Digital Wallet")
        print("4. Cash")
        print("5. Coupon")
        payment_method_input = input("Select Payment Method (Enter the number): ")
        payment_methods = {
            "1": "net banking",
            "2": "credit card",
            "3": "digital wallet",
            "4": "cash",
            "5": "coupon"
        }
        payment_method = payment_methods.get(payment_method_input, "").lower()
        if not payment_method:
            raise ValueError("Invalid payment method selected.")

        # Create the ticket instance with default discount from admin
        ticket_id = Utils.generate_unique_id()
        ticket = Ticket(
            ticket_id,
            ticket_type,
            ticket_info['price'],
            ticket_info['validity'],
            visit_date,
            default_discount=ticket_info.get('discount', 0.0)
        )

        # Apply discounts and set validity inside ticket
        ticket.apply_discounts(user, num_tickets, payment_method)
        ticket.set_validity_dates(user)

        # Validate ticket conditions
        ticket.validate(
            group_size=num_tickets,
            adult_present=adult_present,
            tickets_sold_today=0  # Implement tracking of tickets sold today if needed
        )

        # Calculate total price
        total_price = ticket.price * num_tickets

        # Process payment
        payment_id = Utils.generate_unique_id()
        payment = Payment(payment_id, payment_method)
        payment_success = payment.process_payment(total_price)
        if not payment_success:
            raise ValueError("Payment failed!")

        # Update sales report
        update_sales_report(user, ticket, num_tickets)


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
            user.purchase_ticket(individual_ticket)

        # Save data
        DataStorage.save_to_file(users, FILE_PATH_USERS)

        # Show discount applied and validity
        print(f"Discount Applied: {ticket.discount * 100}%, Total Price: {total_price} DHS")
        print(f"Ticket Validity: From {ticket.validity_start_date} to {ticket.validity_end_date}")

    except Exception as e:
        print(f"Error: {e}")

# Admin Management
def admin_login():
    """Handle admin login."""
    try:
        email = input("Enter admin email: ")
        password = input("Enter admin password: ")
        if email == "admin@adventureland.com" and password == "admin123":
            print("Welcome, Admin!")
            admin_menu()
        else:
            print("Invalid admin credentials!")
    except Exception as e:
        print(f"Error: {e}")

def admin_menu():
    """Display the admin menu."""
    while True:
        print("\nAdmin Menu:")
        print("1. View Sales Reports")
        print("2. Manage Discounts")
        print("3. Logout")
        
        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                view_sales_reports()
            elif choice == 2:
                manage_discounts()
            elif choice == 3:
                print("Logging out...")
                break
            else:
                print("Invalid choice! Please enter a valid option.")
        except ValueError:
            print("Invalid input! Please enter a number.")

# Sales Reports
def view_sales_reports():
    """Display all sales reports with transaction details."""
    try:
        if not sales_reports:
            print("No sales reports available.")
            return

        for report in sales_reports.values():
            print(report)
    except Exception as e:
        print(f"Error: {e}")

def update_sales_report(user, ticket, quantity):
    """Update the daily sales report with the transaction."""
    today = Utils.get_today_date()
    report = sales_reports.get(today)
    if not report:
        report_id = Utils.generate_unique_id()
        report = SalesReport(report_id, today)
        sales_reports[today] = report

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
    DataStorage.save_to_file(sales_reports, FILE_PATH_SALES_REPORTS)

# Discounts Management
def manage_discounts():
    """Allow the admin to modify ticket discounts."""
    try:
        print("\nAvailable Tickets:")
        for ticket_type in tickets.keys():
            print(f"- {ticket_type}")

        ticket_type_input = input("Enter the ticket type to modify discount: ")
        ticket_type = ticket_type_input.strip()
        if ticket_type not in tickets:
            raise ValueError("Invalid ticket type!")

        discount_input = input("Enter the new discount (e.g., 0.15 for 15%): ")
        discount = float(discount_input)
        if not (0 <= discount <= 1):
            raise ValueError("Discount must be between 0 and 1.")

        tickets[ticket_type]['discount'] = discount
        DataStorage.save_to_file(tickets, FILE_PATH_TICKETS)
        print(f"Discount updated for {ticket_type}.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    
    main_menu()
