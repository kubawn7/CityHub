class Order:
    def __init__(self, order_id, user_id, ticket_id):
        self.order_id = order_id
        self.user_id = user_id
        self.ticket_id = ticket_id
        self.status = "PENDING"

    def complete_order(self):
        self.status = "PAID"

    def __str__(self):
        return f"Order #{self.order_id} | Status: {self.status}"