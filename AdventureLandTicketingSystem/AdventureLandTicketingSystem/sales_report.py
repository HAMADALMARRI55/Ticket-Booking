class SalesReport:
    def __init__(self, report_id, date, total_sales, tickets_sold):
        """
        Initialize a SalesReport object.
        """
        self.report_id = report_id
        self.date = date
        self.total_sales = total_sales
        self.tickets_sold = tickets_sold

    def __str__(self):
        """
        String representation of the sales report.
        """
        return f"Date: {self.date}, Total Sales: {self.total_sales}, Tickets Sold: {self.tickets_sold}"
