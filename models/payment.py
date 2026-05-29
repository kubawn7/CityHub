class Payment:
    def __init__(self, payment_id, order_id, amount):
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.status = "SUCCESS"

    def __str__(self):
        return f"Payment #{self.payment_id} | {self.amount} PLN | {self.status}"