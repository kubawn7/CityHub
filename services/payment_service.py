from data_store import payments
from models.payment import Payment
from utils.generator import generate_id


class PaymentService:

    @staticmethod
    def process_payment(order, amount):

        payment = Payment(
            generate_id(),
            order.order_id,
            amount
        )

        payments.append(payment)

        order.complete_order()

        print("Płatność zakończona sukcesem")
        return payment