# File paths for data storage
FILE_PATH_USERS = "data/users.pkl"
FILE_PATH_TICKETS = "data/tickets.pkl"
FILE_PATH_SALES_REPORTS = "data/sales_reports.pkl"

# Ticket discount constants
DISCOUNT_ON_TWO_DAY_PASS = 0.10  # 10%
DISCOUNT_ON_GROUP_TICKET = 0.20  # 20%
DISCOUNT_ON_ANNUAL_RENEWAL = 0.15  # 15%

# Ticket types and pricing
TICKET_PRICES = {
    "Single-Day Pass": 275,
    "Two-Day Pass": 480,
    "Annual Membership": 1840,
    "Child Ticket": 185,
    "Group Ticket (10+)": 220,
    "VIP Experience Pass": 550,
}

# Ticket validity
TICKET_VALIDITY = {
    "Single-Day Pass": "1 Day",
    "Two-Day Pass": "2 Days",
    "Annual Membership": "1 Year",
    "Child Ticket": "1 Day",
    "Group Ticket (10+)": "1 Day",
    "VIP Experience Pass": "1 Day",
}

# General limits and settings
MAX_TICKETS_PER_USER = 10
MIN_GROUP_SIZE_FOR_DISCOUNT = 20
