from data_store import tickets, orders
from models.ticket import Ticket
from models.order import Order
from utils.generator import generate_id


class TicketService:

    @staticmethod
    def create_ticket(event_id, ticket_type, price, quantity=1):
        if ticket_type not in ["Standard", "VIP"]:
            print("Nieprawidłowy typ biletu. Dostępne: Standard, VIP")
            return None
            
        created_tickets = []
        for _ in range(quantity):
            ticket = Ticket(
                generate_id(),
                event_id,
                ticket_type,
                price
            )
            tickets.append(ticket)
            created_tickets.append(ticket)

        print(f"Pula została utworzona: {quantity} bilet(ów) typu {ticket_type}")
        return created_tickets

    @staticmethod
    def list_tickets():
        for ticket in tickets:
            print(ticket)

    @staticmethod
    def get_available_tickets(event_id):
        sold_ticket_ids = [order.ticket_id for order in orders]
        available_tickets = [t for t in tickets if t.event_id == event_id and t.ticket_id not in sold_ticket_ids]
        return available_tickets

    @staticmethod
    def buy_ticket(user_id, ticket_id):
        for order in orders:
            if order.ticket_id == ticket_id:
                print("Ten bilet został już wykupiony.")
                return None

        ticket = None
        for t in tickets:
            if t.ticket_id == ticket_id:
                ticket = t
                break

        if ticket is None:
            print("Nie znaleziono biletu")
            return None

        order = Order(
            generate_id(),
            user_id,
            ticket_id
        )
        orders.append(order)

        print("Zamówienie zostało utworzone")
        return order

    @staticmethod
    def validate_ticket(ticket_id):

        ticket = next((t for t in tickets if t.ticket_id == ticket_id), None)
        if not ticket:
            print("Nie znaleziono biletu w systemie.")
            return False
            

        order = next((o for o in orders if o.ticket_id == ticket_id), None)
        if not order:
            print("Odmowa dostępu: Ten bilet nie został sprzedany (jest wciąż w puli).")
            return False
            

        if order.status != "PAID":
             print("Odmowa dostępu: Bilet nie został opłacony!")
             return False


        if ticket.is_used:
            print("Odmowa dostępu: Bilet został już wykorzystany na bramce!")
            return False

        ticket.is_used = True
        print("Bilet poprawny. Witamy na wydarzeniu!")
        return True