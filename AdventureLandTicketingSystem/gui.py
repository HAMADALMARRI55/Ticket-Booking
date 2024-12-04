# gui.py

import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from data_storage import DataStorage
from constants import FILE_PATH_USERS, FILE_PATH_TICKETS, FILE_PATH_SALES_REPORTS
from user import User
from admin import Admin
from ticket import Ticket
from payment import Payment
from sales_report import SalesReport, Transaction
from utils import Utils

# Load data
users = DataStorage.load_from_file(FILE_PATH_USERS)
tickets = DataStorage.load_from_file(FILE_PATH_TICKETS)
sales_reports = DataStorage.load_from_file(FILE_PATH_SALES_REPORTS)

# Ensure all SalesReport objects have the 'transactions' attribute
if sales_reports:
    for report in sales_reports.values():
        if not hasattr(report, 'transactions'):
            report.transactions = []

class TicketingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adventure Land Theme Park Ticketing System")
        self.root.geometry("600x600")
        self.current_user = None  # To keep track of the logged-in user
        self.create_welcome_frame()

    def create_welcome_frame(self):
        self.clear_frames()
        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.welcome_frame, text="Welcome to Adventure Land Theme Park", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.welcome_frame, text="Login", command=self.create_login_frame, width=20).pack(pady=10)
        tk.Button(self.welcome_frame, text="Create Account", command=self.create_account_frame, width=20).pack(pady=10)
        tk.Button(self.welcome_frame, text="Admin Login", command=self.create_admin_login_frame, width=20).pack(pady=10)
        tk.Button(self.welcome_frame, text="Exit", command=self.root.quit, width=20).pack(pady=10)

    def clear_frames(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_account_frame(self):
        self.clear_frames()
        self.account_frame = tk.Frame(self.root)
        self.account_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.account_frame, text="Create a New Account", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.account_frame, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self.account_frame)
        self.name_entry.pack()

        tk.Label(self.account_frame, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.account_frame)
        self.email_entry.pack()

        tk.Label(self.account_frame, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.account_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.account_frame, text="Create Account", command=self.create_account).pack(pady=10)
        tk.Button(self.account_frame, text="Back", command=self.create_welcome_frame).pack()

    def create_account(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not Utils.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        if email in users:
            messagebox.showerror("Error", "An account with this email already exists.")
            return

        user_id = Utils.generate_unique_id()
        new_user = User(user_id, name, email, password)
        users[email] = new_user
        DataStorage.save_to_file(users, FILE_PATH_USERS)
        messagebox.showinfo("Success", "Account created successfully!")
        self.create_login_frame()

    def create_login_frame(self):
        self.clear_frames()
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.login_frame, text="User Login", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.login_frame, text="Email:").pack(pady=5)
        self.login_email_entry = tk.Entry(self.login_frame)
        self.login_email_entry.pack()

        tk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.pack()

        tk.Button(self.login_frame, text="Login", command=self.user_login).pack(pady=10)
        tk.Button(self.login_frame, text="Back", command=self.create_welcome_frame).pack()

    def user_login(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        user = users.get(email)
        if user and user.password == password:
            user.load_purchase_history(user.purchase_history)
            self.current_user = user
            messagebox.showinfo("Success", f"Welcome, {user.name}!")
            self.create_user_dashboard()
        else:
            messagebox.showerror("Error", "Invalid email or password!")

    def create_user_dashboard(self):
        self.clear_frames()
        self.user_dashboard = tk.Frame(self.root)
        self.user_dashboard.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.user_dashboard, text=f"Welcome, {self.current_user.name}", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.user_dashboard, text="View Purchase History", command=self.view_purchase_history, width=25).pack(pady=10)
        tk.Button(self.user_dashboard, text="Purchase Ticket", command=self.create_purchase_frame, width=25).pack(pady=10)
        tk.Button(self.user_dashboard, text="Logout", command=self.logout, width=25).pack(pady=10)

    def logout(self):
        self.current_user = None
        self.create_welcome_frame()

    def view_purchase_history(self):
        self.clear_frames()
        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.history_frame, text="Purchase History", font=("Arial", 16)).pack(pady=20)

        if not self.current_user.purchase_history:
            tk.Label(self.history_frame, text="No tickets purchased yet.").pack()
        else:
            history_text = scrolledtext.ScrolledText(self.history_frame, width=70, height=20)
            history_text.pack()
            for ticket in self.current_user.purchase_history:
                ticket_info = (
                    f"Ticket ID: {ticket.ticket_id}\n"
                    f"Ticket Type: {ticket.ticket_type}\n"
                    f"Price: {ticket.price} DHS\n"
                    f"Validity: From {ticket.validity_start_date} to {ticket.validity_end_date}\n"
                    f"Visit Date: {ticket.visit_date}\n"
                    f"Discount Applied: {ticket.discount * 100}%\n"
                    "----------------------------------------\n"
                )
                history_text.insert(tk.END, ticket_info)
            history_text.configure(state='disabled')

        tk.Button(self.history_frame, text="Back", command=self.create_user_dashboard).pack(pady=10)

    def create_purchase_frame(self):
        self.clear_frames()
        self.purchase_frame = tk.Frame(self.root)
        self.purchase_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.purchase_frame, text="Purchase Ticket", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.purchase_frame, text="Select Ticket Type:").pack(pady=5)
        self.ticket_var = tk.StringVar(self.purchase_frame)
        self.ticket_var.set("Select Ticket")
        ticket_options = list(tickets.keys())
        tk.OptionMenu(self.purchase_frame, self.ticket_var, *ticket_options).pack()

        tk.Label(self.purchase_frame, text="Visit Date (YYYY-MM-DD):").pack(pady=5)
        self.visit_date_entry = tk.Entry(self.purchase_frame)
        self.visit_date_entry.pack()

        tk.Label(self.purchase_frame, text="Number of Tickets:").pack(pady=5)
        self.num_tickets_entry = tk.Entry(self.purchase_frame)
        self.num_tickets_entry.pack()

        tk.Label(self.purchase_frame, text="Select Payment Method:").pack(pady=5)
        self.payment_var = tk.StringVar(self.purchase_frame)
        self.payment_var.set("Select Payment Method")
        payment_methods = ["Net Banking", "Credit Card", "Digital Wallet", "Cash", "Coupon"]
        tk.OptionMenu(self.purchase_frame, self.payment_var, *payment_methods).pack()

        tk.Button(self.purchase_frame, text="Purchase", command=self.purchase_ticket).pack(pady=10)
        tk.Button(self.purchase_frame, text="Back", command=self.create_user_dashboard).pack()

    def purchase_ticket(self):
        ticket_type = self.ticket_var.get()
        visit_date = self.visit_date_entry.get()
        num_tickets = self.num_tickets_entry.get()
        payment_method = self.payment_var.get()

        # Input validation
        if ticket_type == "Select Ticket":
            messagebox.showerror("Error", "Please select a ticket type.")
            return
        if not Utils.validate_date(visit_date):
            messagebox.showerror("Error", "Invalid or past date!")
            return
        try:
            num_tickets = int(num_tickets)
            if num_tickets <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Number of tickets must be a positive integer.")
            return
        if payment_method == "Select Payment Method":
            messagebox.showerror("Error", "Please select a payment method.")
            return

        try:
            ticket_info = tickets.get(ticket_type)
            adult_present = True  # Assume adult is present for simplicity

            # For Child Ticket, ensure an adult ticket is purchased
            if ticket_type == "Child Ticket":
                adult_present = any(
                    t.ticket_type in ["Single-Day Pass", "Two-Day Pass", "Annual Membership", "VIP Experience Pass"]
                    for t in self.current_user.purchase_history
                )
                if not adult_present:
                    response = messagebox.askyesno("Adult Ticket Required", "An adult ticket must be purchased with a Child Ticket. Would you like to purchase an adult ticket first?")
                    if response:
                        self.create_purchase_frame()
                        return
                    else:
                        messagebox.showerror("Error", "Cannot purchase a Child Ticket without an accompanying adult ticket.")
                        return

            # Create the ticket instance with default discount
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
            payment_method_key = payment_method.lower()
            payment_method_key = payment_method_key.replace(" ", " ")
            ticket.apply_discounts(self.current_user, num_tickets, payment_method_key)
            ticket.set_validity_dates(self.current_user)

            # Validate ticket conditions
            ticket.validate(
                group_size=num_tickets,
                adult_present=adult_present,
                tickets_sold_today=0  # Implement tracking if needed
            )

            # Calculate total price
            total_price = ticket.price * num_tickets

            # Process payment
            payment_id = Utils.generate_unique_id()
            payment = Payment(payment_id, payment_method_key)
            payment_success = payment.process_payment(total_price)
            if not payment_success:
                messagebox.showerror("Error", "Payment failed!")
                return

            # Update sales report
            update_sales_report(self.current_user, ticket, num_tickets)

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
                self.current_user.purchase_ticket(individual_ticket)

            # Save data
            DataStorage.save_to_file(users, FILE_PATH_USERS)

            # Show success message with details
            discount_percentage = ticket.discount * 100
            messagebox.showinfo(
                "Success",
                f"Ticket purchased successfully!\n\n"
                f"Discount Applied: {discount_percentage}%\n"
                f"Total Price: {total_price} DHS\n"
                f"Validity: From {ticket.validity_start_date} to {ticket.validity_end_date}"
            )
            self.create_user_dashboard()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_admin_login_frame(self):
        self.clear_frames()
        self.admin_login_frame = tk.Frame(self.root)
        self.admin_login_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.admin_login_frame, text="Admin Login", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.admin_login_frame, text="Email:").pack(pady=5)
        self.admin_email_entry = tk.Entry(self.admin_login_frame)
        self.admin_email_entry.pack()

        tk.Label(self.admin_login_frame, text="Password:").pack(pady=5)
        self.admin_password_entry = tk.Entry(self.admin_login_frame, show="*")
        self.admin_password_entry.pack()

        tk.Button(self.admin_login_frame, text="Login", command=self.admin_login).pack(pady=10)
        tk.Button(self.admin_login_frame, text="Back", command=self.create_welcome_frame).pack()

    def admin_login(self):
        email = self.admin_email_entry.get()
        password = self.admin_password_entry.get()
        if email == "admin@adventureland.com" and password == "admin123":
            messagebox.showinfo("Success", "Welcome, Admin!")
            self.create_admin_dashboard()
        else:
            messagebox.showerror("Error", "Invalid admin credentials!")

    def create_admin_dashboard(self):
        self.clear_frames()
        self.admin_dashboard = tk.Frame(self.root)
        self.admin_dashboard.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.admin_dashboard, text="Admin Dashboard", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.admin_dashboard, text="View Sales Reports", command=self.view_sales_reports, width=25).pack(pady=10)
        tk.Button(self.admin_dashboard, text="Manage Discounts", command=self.manage_discounts_frame, width=25).pack(pady=10)
        tk.Button(self.admin_dashboard, text="Logout", command=self.create_welcome_frame, width=25).pack(pady=10)

    def view_sales_reports(self):
        self.clear_frames()
        self.reports_frame = tk.Frame(self.root)
        self.reports_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.reports_frame, text="Sales Reports", font=("Arial", 16)).pack(pady=20)

        if not sales_reports:
            tk.Label(self.reports_frame, text="No sales reports available.").pack()
        else:
            reports_text = scrolledtext.ScrolledText(self.reports_frame, width=70, height=25)
            reports_text.pack()
            for report in sales_reports.values():
                reports_text.insert(tk.END, str(report) + "\n")
            reports_text.configure(state='disabled')

        tk.Button(self.reports_frame, text="Back", command=self.create_admin_dashboard).pack(pady=10)

    def manage_discounts_frame(self):
        self.clear_frames()
        self.manage_discounts_frame = tk.Frame(self.root)
        self.manage_discounts_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.manage_discounts_frame, text="Manage Discounts", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.manage_discounts_frame, text="Select Ticket Type:").pack(pady=5)
        self.discount_ticket_var = tk.StringVar(self.manage_discounts_frame)
        self.discount_ticket_var.set("Select Ticket")
        ticket_options = list(tickets.keys())
        tk.OptionMenu(self.manage_discounts_frame, self.discount_ticket_var, *ticket_options).pack()

        tk.Label(self.manage_discounts_frame, text="Enter New Discount (e.g., 0.15 for 15%):").pack(pady=5)
        self.new_discount_entry = tk.Entry(self.manage_discounts_frame)
        self.new_discount_entry.pack()

        tk.Button(self.manage_discounts_frame, text="Update Discount", command=self.update_discount).pack(pady=10)
        tk.Button(self.manage_discounts_frame, text="Back", command=self.create_admin_dashboard).pack()

    def update_discount(self):
        ticket_type = self.discount_ticket_var.get()
        discount_str = self.new_discount_entry.get()

        if ticket_type == "Select Ticket":
            messagebox.showerror("Error", "Please select a ticket type.")
            return
        try:
            discount = float(discount_str)
            if not (0 <= discount <= 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Discount must be a decimal between 0 and 1.")
            return

        tickets[ticket_type]['discount'] = discount
        DataStorage.save_to_file(tickets, FILE_PATH_TICKETS)
        messagebox.showinfo("Success", f"Discount updated for {ticket_type}.")
        self.create_admin_dashboard()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketingApp(root)
    root.mainloop()
