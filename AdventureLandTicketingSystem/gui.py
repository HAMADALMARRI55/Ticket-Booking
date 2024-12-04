"""
GUI Module for the Adventure Land Theme Park Ticketing System.

This module creates a graphical user interface using Tkinter for users and admins
to interact with the ticketing system. It allows users to create accounts, log in,
purchase tickets, and view their purchase history. Admins can log in to view sales
reports and manage discounts.
"""



import tkinter as tk
from tkinter import messagebox, ttk
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

# SalesReport objects have the 'transactions' attribute
if sales_reports:
    for report in sales_reports.values():
        if not hasattr(report, 'transactions'):
            report.transactions = []

class TicketingApp:
    """
    The main GUI application class for the Adventure Land Theme Park Ticketing System.

    This class initializes the main window and handles all GUI-related functionalities,
    including user registration, login, ticket purchasing, and admin operations.
    """
    def __init__(self, root):
        """Initialize the application window and set up styles."""
        self.root = root
        self.root.title("Adventure Land Theme Park")
        self.root.geometry("700x700")
        self.root.configure(bg='#F0F4F8')

        # Custom style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure styles
        self.style.configure('TButton',
                             font=('Helvetica', 10))
        self.style.configure('TLabel',
                             font=('Helvetica', 12))
        self.style.configure('Header.TLabel',
                             font=('Arial', 16))
        self.style.configure('TFrame',
                             background='#F0F4F8')
        self.style.configure('Treeview',
                             font=('Helvetica', 10))
        self.style.configure('Treeview.Heading',
                             font=('Helvetica', 10, 'bold'))

        self.current_user = None
        self.create_welcome_frame()

    def create_welcome_frame(self):
        """Create the welcome frame with options to login, create an account, or admin login."""
        self.clear_frames()
        self.welcome_frame = ttk.Frame(self.root)
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.welcome_frame, text="Welcome to Adventure Land Theme Park", style='Header.TLabel').pack(pady=20)

        ttk.Button(self.welcome_frame, text="Login", command=self.create_login_frame, width=20).pack(pady=10)
        ttk.Button(self.welcome_frame, text="Create Account", command=self.create_account_frame, width=20).pack(pady=10)
        ttk.Button(self.welcome_frame, text="Admin Login", command=self.create_admin_login_frame, width=20).pack(pady=10)
        ttk.Button(self.welcome_frame, text="Exit", command=self.root.quit, width=20).pack(pady=10)

    def clear_frames(self):
        """Clear all frames from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_account_frame(self):
        """Display the account creation frame for new users to sign up."""
        self.clear_frames()
        self.account_frame = ttk.Frame(self.root)
        self.account_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.account_frame, text="Create a New Account", style='Header.TLabel').pack(pady=20)

        ttk.Label(self.account_frame, text="Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self.account_frame)
        self.name_entry.pack()

        ttk.Label(self.account_frame, text="Email:").pack(pady=5)
        self.email_entry = ttk.Entry(self.account_frame)
        self.email_entry.pack()

        ttk.Label(self.account_frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.account_frame, show="*")
        self.password_entry.pack()

        ttk.Button(self.account_frame, text="Create Account", command=self.create_account).pack(pady=10)
        ttk.Button(self.account_frame, text="Back", command=self.create_welcome_frame).pack()

    def create_account(self):
        """Handle the creation of a new user account after validating inputs."""
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
        """Display the login frame for existing users to sign in."""
        self.clear_frames()
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.login_frame, text="User Login", style='Header.TLabel').pack(pady=20)

        ttk.Label(self.login_frame, text="Email:").pack(pady=5)
        self.login_email_entry = ttk.Entry(self.login_frame)
        self.login_email_entry.pack()

        ttk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.login_password_entry = ttk.Entry(self.login_frame, show="*")
        self.login_password_entry.pack()

        ttk.Button(self.login_frame, text="Login", command=self.user_login).pack(pady=10)
        ttk.Button(self.login_frame, text="Back", command=self.create_welcome_frame).pack()

    def user_login(self):
        """Handle the login process for existing users after validating inputs."""
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
        """Display the user dashboard with their purchase history."""
        self.clear_frames()
        self.user_dashboard = ttk.Frame(self.root)
        self.user_dashboard.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.user_dashboard, text=f"Welcome, {self.current_user.name}", style='Header.TLabel').pack(pady=20)

        ttk.Button(self.user_dashboard, text="View Purchase History", command=self.view_purchase_history, width=25).pack(pady=10)
        ttk.Button(self.user_dashboard, text="Purchase Ticket", command=self.create_purchase_frame, width=25).pack(pady=10)
        ttk.Button(self.user_dashboard, text="Logout", command=self.logout, width=25).pack(pady=10)

    def logout(self):
        """Clear the current user and display the welcome frame again."""
        self.current_user = None
        self.create_welcome_frame()

    def view_purchase_history(self):
        """Display the user's purchase history in a new frame."""
        self.clear_frames()
        self.history_frame = ttk.Frame(self.root)
        self.history_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.history_frame, text="Purchase History", style='Header.TLabel').pack(pady=20)

        if not self.current_user.purchase_history:
            ttk.Label(self.history_frame, text="No tickets purchased yet.").pack()
        else:
            columns = ('ticket_id', 'ticket_type', 'price', 'validity', 'visit_date', 'discount')
            tree = ttk.Treeview(self.history_frame, columns=columns, show='headings')
            tree.pack(fill=tk.BOTH, expand=True)

            tree.heading('ticket_id', text='Ticket ID')
            tree.heading('ticket_type', text='Ticket Type')
            tree.heading('price', text='Price (DHS)')
            tree.heading('validity', text='Validity')
            tree.heading('visit_date', text='Visit Date')
            tree.heading('discount', text='Discount Applied')

            for ticket in self.current_user.purchase_history:
                validity = f"From {ticket.validity_start_date} to {ticket.validity_end_date}"
                discount_percentage = f"{ticket.discount * 100}%"
                tree.insert('', tk.END, values=(
                    ticket.ticket_id,
                    ticket.ticket_type,
                    ticket.price,
                    validity,
                    ticket.visit_date,
                    discount_percentage
                ))

            # Add vertical scrollbar
            scrollbar = ttk.Scrollbar(self.history_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(self.history_frame, text="Back", command=self.create_user_dashboard).pack(pady=10)

    def create_purchase_frame(self):
        """Create a frame for purchasing tickets."""
        self.clear_frames()
        self.purchase_frame = ttk.Frame(self.root)
        self.purchase_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.purchase_frame, text="Purchase Ticket", style='Header.TLabel').pack(pady=20)

        ttk.Label(self.purchase_frame, text="Select Ticket Type:").pack(pady=5)
        ticket_options = list(tickets.keys())
        self.ticket_var = tk.StringVar()
        self.ticket_combobox = ttk.Combobox(self.purchase_frame, textvariable=self.ticket_var, values=ticket_options, state='readonly')
        self.ticket_combobox.set("Select Ticket")
        self.ticket_combobox.pack()

        ttk.Label(self.purchase_frame, text="Visit Date (YYYY-MM-DD):").pack(pady=5)
        self.visit_date_entry = ttk.Entry(self.purchase_frame)
        self.visit_date_entry.pack()

        ttk.Label(self.purchase_frame, text="Number of Tickets:").pack(pady=5)
        self.num_tickets_entry = ttk.Entry(self.purchase_frame)
        self.num_tickets_entry.pack()

        ttk.Label(self.purchase_frame, text="Select Payment Method:").pack(pady=5)
        payment_methods = ["Net Banking", "Credit Card", "Digital Wallet", "Cash", "Coupon"]
        self.payment_var = tk.StringVar()
        self.payment_combobox = ttk.Combobox(self.purchase_frame, textvariable=self.payment_var, values=payment_methods, state='readonly')
        self.payment_combobox.set("Select Payment Method")
        self.payment_combobox.pack()

        ttk.Button(self.purchase_frame, text="Purchase", command=self.purchase_ticket).pack(pady=10)
        ttk.Button(self.purchase_frame, text="Back", command=self.create_user_dashboard).pack()

    def purchase_ticket(self):
        """Purchase a ticket based on user input."""
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
            adult_present = True  

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
        """Display the admin login frame for admin authentication."""
        self.clear_frames()
        self.admin_login_frame = ttk.Frame(self.root)
        self.admin_login_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.admin_login_frame, text="Admin Login", style='Header.TLabel').pack(pady=20)

        ttk.Label(self.admin_login_frame, text="Email:").pack(pady=5)
        self.admin_email_entry = ttk.Entry(self.admin_login_frame)
        self.admin_email_entry.pack()

        ttk.Label(self.admin_login_frame, text="Password:").pack(pady=5)
        self.admin_password_entry = ttk.Entry(self.admin_login_frame, show="*")
        self.admin_password_entry.pack()

        ttk.Button(self.admin_login_frame, text="Login", command=self.admin_login).pack(pady=10)
        ttk.Button(self.admin_login_frame, text="Back", command=self.create_welcome_frame).pack()

    def admin_login(self):
        """Authenticate admin user and display admin dashboard if successful."""
        email = self.admin_email_entry.get()
        password = self.admin_password_entry.get()
        if email == "admin@adventureland.com" and password == "admin123":
            messagebox.showinfo("Success", "Welcome, Admin!")
            self.create_admin_dashboard()
        else:
            messagebox.showerror("Error", "Invalid admin credentials!")

    def create_admin_dashboard(self):
        """Display the admin dashboard for admin to manage users and tickets."""
        self.clear_frames()
        self.admin_dashboard = ttk.Frame(self.root)
        self.admin_dashboard.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.admin_dashboard, text="Admin Dashboard", style='Header.TLabel').pack(pady=20)

        ttk.Button(self.admin_dashboard, text="View Sales Reports", command=self.view_sales_reports, width=25).pack(pady=10)
        ttk.Button(self.admin_dashboard, text="Manage Discounts", command=self.manage_discounts_frame, width=25).pack(pady=10)
        ttk.Button(self.admin_dashboard, text="Logout", command=self.create_welcome_frame, width=25).pack(pady=10)

    def view_sales_reports(self):
        """Display the sales reports for admin to view sales data."""
        self.clear_frames()
        self.reports_frame = ttk.Frame(self.root)
        self.reports_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.reports_frame, text="Sales Reports", style='Header.TLabel').pack(pady=20)

        if not sales_reports:
            ttk.Label(self.reports_frame, text="No sales reports available.").pack()
        else:
            # Create a Treeview
            columns = ('date', 'transaction_id', 'customer_name', 'ticket_type', 'quantity', 'total_price', 'date_of_purchase')
            tree = ttk.Treeview(self.reports_frame, columns=columns, show='headings')
            tree.pack(fill=tk.BOTH, expand=True)

            tree.heading('date', text='Date')
            tree.heading('transaction_id', text='Transaction ID')
            tree.heading('customer_name', text='Customer Name')
            tree.heading('ticket_type', text='Ticket Type')
            tree.heading('quantity', text='Quantity')
            tree.heading('total_price', text='Total Price')
            tree.heading('date_of_purchase', text='Date of Purchase')

            for report_date, report in sales_reports.items():
                for transaction in report.transactions:
                    tree.insert('', tk.END, values=(
                        report_date,
                        transaction.transaction_id,
                        transaction.customer_name,
                        transaction.ticket_type,
                        transaction.quantity,
                        transaction.total_price,
                        transaction.date_of_purchase
                    ))

            # Add vertical scrollbar
            scrollbar = ttk.Scrollbar(self.reports_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(self.reports_frame, text="Back", command=self.create_admin_dashboard).pack(pady=10)

    def manage_discounts_frame(self):
        """Display the discounts management frame for admin to manage discounts."""
        self.clear_frames()
        self.manage_discounts_frame = ttk.Frame(self.root)
        self.manage_discounts_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.manage_discounts_frame, text="Manage Discounts", style='Header.TLabel').pack(pady=20)

        ttk.Label(self.manage_discounts_frame, text="Select Ticket Type:").pack(pady=5)
        ticket_options = list(tickets.keys())
        self.discount_ticket_var = tk.StringVar()
        self.discount_ticket_combobox = ttk.Combobox(self.manage_discounts_frame, textvariable=self.discount_ticket_var, values=ticket_options, state='readonly')
        self.discount_ticket_combobox.set("Select Ticket")
        self.discount_ticket_combobox.pack()

        ttk.Label(self.manage_discounts_frame, text="Enter New Discount (e.g., 0.15 for 15%):").pack(pady=5)
        self.new_discount_entry = ttk.Entry(self.manage_discounts_frame)
        self.new_discount_entry.pack()

        ttk.Button(self.manage_discounts_frame, text="Update Discount", command=self.update_discount).pack(pady=10)
        ttk.Button(self.manage_discounts_frame, text="Back", command=self.create_admin_dashboard).pack()

    def update_discount(self):
        """Update the discount for the selected ticket type."""
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
