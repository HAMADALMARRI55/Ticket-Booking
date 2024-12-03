from user import User
from admin import Admin
from ticket import Ticket
from payment import Payment
from sales_report import SalesReport
from data_storage import DataStorage
from utils import Utils
from constants import FILE_PATH_USERS, FILE_PATH_TICKETS, FILE_PATH_SALES_REPORTS

def main():
    print("Welcome to Adventure Land Ticket Booking System!")
    users = DataStorage.load_from_file(FILE_PATH_USERS)
    tickets = DataStorage.load_from_file(FILE_PATH_TICKETS)
    sales_reports = DataStorage.load_from_file(FILE_PATH_SALES_REPORTS)

    while True:
        print("\nMain Menu:")
        print("1. Create User Account")
        print("2. User Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
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

        elif choice == "2":
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

                    if user_choice == "1":
                        user.view_purchase_history()
                    elif user_choice == "2":
                        print("Available Tickets:")
                        for ticket_type, price in tickets.items():
                            print(f"{ticket_type}: {price['price']} DHS, Validity: {price['validity']}")
                        ticket_type = input("Enter the ticket type: ")
                        if ticket_type in tickets:
                            ticket_id = Utils.generate_unique_id()
                            ticket = Ticket(
                                ticket_id,
                                ticket_type,
                                tickets[ticket_type]["price"],
                                tickets[ticket_type]["validity"]
                            )
                            user.purchase_ticket(ticket)
                            DataStorage.save_to_file(users, FILE_PATH_USERS)
                        else:
                            print("Invalid ticket type!")
                    elif user_choice == "3":
                        break
                    else:
                        print("Invalid choice!")

        elif choice == "3":
            email = input("Enter admin email: ")
            password = input("Enter admin password: ")
            # Simulate admin login (for demo purposes, use hardcoded admin credentials)
            if email == "admin@adventureland.com" and password == "admin123":
                admin = Admin("0", "Admin", email, password)
                print(f"Welcome, {admin.name}!")
                while True:
                    print("\nAdmin Menu:")
                    print("1. View Sales Reports")
                    print("2. Manage Discounts")
                    print("3. Logout")
                    admin_choice = input("Enter your choice: ")

                    if admin_choice == "1":
                        admin.view_sales(sales_reports)
                    elif admin_choice == "2":
                        ticket_type = input("Enter the ticket type to modify discount: ")
                        if ticket_type in tickets:
                            discount = float(input("Enter the new discount (e.g., 0.15 for 15%): "))
                            tickets[ticket_type]["discount"] = discount
                            DataStorage.save_to_file(tickets, FILE_PATH_TICKETS)
                            print(f"Discount updated for {ticket_type}.")
                        else:
                            print("Invalid ticket type!")
                    elif admin_choice == "3":
                        break
                    else:
                        print("Invalid choice!")

        elif choice == "4":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
