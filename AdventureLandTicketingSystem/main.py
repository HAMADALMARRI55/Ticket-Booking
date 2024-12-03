from user import User
from admin import Admin
from ticket import Ticket
from payment import Payment
from sales_report import SalesReport
from data_storage import DataStorage
from utils import Utils
from constants import FILE_PATH_USERS, FILE_PATH_TICKETS, FILE_PATH_SALES_REPORTS, TICKET_PRICES, TICKET_VALIDITY

def initialize_tickets():
    """
    Initialize ticket data if the tickets file doesn't exist.
    """
    tickets = DataStorage.load_from_file(FILE_PATH_TICKETS)
    if not tickets:
        print("Initializing ticket data...")
        for ticket_type, price in TICKET_PRICES.items():
            tickets[ticket_type] = {
                "price": price,
                "validity": TICKET_VALIDITY[ticket_type],
                "discount": 0.0  # Default no discount
            }
        DataStorage.save_to_file(tickets, FILE_PATH_TICKETS)
        print("Ticket data initialized.")
    return tickets

def main():
    print("Welcome to Adventure Land Ticket Booking System!")
    users = DataStorage.load_from_file(FILE_PATH_USERS)
    tickets = initialize_tickets()
    sales_reports = DataStorage.load_from_file(FILE_PATH_SALES_REPORTS)

    while True:
        print("\nMain Menu:")
        print("1. Create User Account")
        print("2. User Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":  # Create User Account
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            if Utils.validate_email(email):
                user_id = Utils.generate_unique_id()
                users[email] = User(user_id, name, email, password)
                DataStorage.save_to_file(users, FILE_PATH_USERS)
                print("Account created successfully!")
            else:
                print("Invalid email format!")

        elif choice == "2":  # User Login
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            if email in users and users[email].login(email, password):
                user = users[email]
                print(f"Welcome, {user.name}!")
                while True:
                    print("\nUser Menu:")
                    print("1. View Purchase History")
                    print("2. Purchase Ticket")
                    print("3. Logout")
                    user_choice = input("Enter your choice: ")

                    if user_choice == "1":  # View Purchase History
                        user.view_purchase_history()

                    elif user_choice == "2":  # Purchase Ticket
                        print("Available Tickets:")
                        for ticket_type, details in tickets.items():
                            print(f"{ticket_type}: {details['price']} DHS, Validity: {details['validity']}")
                        ticket_type = input("Enter the ticket type: ")
                        if ticket_type in tickets:
                            # Apply the discount if available
                            original_price = tickets[ticket_type]["price"]
                            discount = tickets[ticket_type]["discount"]
                            discounted_price = original_price * (1 - discount)

                            print(f"Original Price: {original_price} DHS")
                            if discount > 0:
                                print(f"Discount Applied: {discount * 100}%")
                                print(f"Discounted Price: {discounted_price} DHS")
                            else:
                                print("No discount available for this ticket.")

                            # Prompt for visit date
                            visit_date = input("Enter the visit date (YYYY-MM-DD): ")
                            if not Utils.validate_date(visit_date):
                                print("Invalid date format or past date. Please try again.")
                                return

                            # Prompt for payment method
                            print("Select a payment method:")
                            print("1. Credit Card")
                            print("2. Digital Wallet")
                            payment_choice = input("Enter your choice: ")
                            payment_method = "Credit Card" if payment_choice == "1" else "Digital Wallet"

                            # Process payment
                            payment_id = Utils.generate_unique_id()
                            payment = Payment(payment_id, payment_method)
                            if not payment.process_payment(discounted_price):
                                print("Payment failed. Please try again.")
                                return

                            # Create the ticket and save to purchase history
                            ticket_id = Utils.generate_unique_id()
                            ticket = Ticket(
                                ticket_id,
                                ticket_type,
                                discounted_price,
                                tickets[ticket_type]["validity"]
                            )
                            user.purchase_ticket(ticket)
                            DataStorage.save_to_file(users, FILE_PATH_USERS)

                            # Update Sales Report
                            today = str(Utils.get_today_date())
                            if today not in sales_reports:
                                sales_reports[today] = SalesReport(
                                    report_id=Utils.generate_unique_id(),
                                    date=today,
                                    total_sales=0,
                                    tickets_sold=0
                                )
                            sales_reports[today].total_sales += discounted_price
                            sales_reports[today].tickets_sold += 1
                            DataStorage.save_to_file(sales_reports, FILE_PATH_SALES_REPORTS)

                            print(f"Ticket '{ticket_type}' purchased successfully for {discounted_price} DHS!")
                            print(f"Visit Date: {visit_date}")
                            print(f"Payment Method: {payment_method}")
                        else:
                            print("Invalid ticket type!")

                    elif user_choice == "3":  # Logout
                        break
                    else:
                        print("Invalid choice!")

        elif choice == "3":  # Admin Login
            email = input("Enter admin email: ")
            password = input("Enter admin password: ")
            if email == "admin@adventureland.com" and password == "admin123":
                admin = Admin("0", "Admin", email, password)
                print(f"Welcome, {admin.name}!")
                while True:
                    print("\nAdmin Menu:")
                    print("1. View Sales Reports")
                    print("2. Manage Discounts")
                    print("3. Logout")
                    admin_choice = input("Enter your choice: ")

                    if admin_choice == "1":  # View Sales Reports
                        if sales_reports:
                            print("Sales Reports:")
                            for report in sales_reports.values():
                                print(report)
                        else:
                            print("No sales reports available.")

                    elif admin_choice == "2":  # Manage Discounts
                        ticket_type = input("Enter the ticket type to modify discount: ")
                        if ticket_type in tickets:
                            discount_input = input("Enter the new discount (e.g., 0.15 for 15% or 15%): ").strip()
                            try:
                                if "%" in discount_input:
                                    discount = float(discount_input.replace("%", "").strip()) / 100
                                else:
                                    discount = float(discount_input)
                                tickets[ticket_type]["discount"] = discount
                                DataStorage.save_to_file(tickets, FILE_PATH_TICKETS)
                                print(f"Discount updated for {ticket_type}.")
                            except ValueError:
                                print("Invalid discount format! Please enter a valid decimal or percentage.")
                        else:
                            print("Invalid ticket type!")

                    elif admin_choice == "3":  # Logout
                        break
                    else:
                        print("Invalid choice!")

        elif choice == "4":  # Exit
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
