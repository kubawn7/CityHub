class Ticket:
    def __init__(self, ticket_id, event_id, ticket_type, price):
        self.ticket_id = ticket_id
        self.event_id = event_id
        self.ticket_type = ticket_type
        self.price = price
        self.is_used = False

    def __str__(self):
        status = "USED" if self.is_used else "ACTIVE"
        return f"Ticket #{self.ticket_id} | {self.ticket_type} | {self.price} PLN | {status}"