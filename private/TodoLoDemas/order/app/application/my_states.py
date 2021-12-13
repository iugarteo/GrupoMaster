from .state import State
from .publisher import publish_event
from . import order

# Start of our states
class deliveryChecking(State):
    """
    The state which indicates order is checking the delivery address
    """
    def __init__(self, order):
        self.order = order
        print('Processing current state:', str(self))
        message = {"orderId": order.id, "zipCode": order.zip_code, "topic": "checkAddress"}
        publish_event("checkAddress", message)


    def on_event(self, event):
        if event == 'Accepted':
            return paymentChecking(self.order)
        elif event == 'Declined':
            return orderDeclined(self.order)

        return self

class paymentChecking(State):
    """
    The state which indicates order is checking account money
    """
    def __init__(self, order):
        self.order = order
        print('Processing current state:', str(self))
        precio = order.price_total
        message = {"price": precio, "client_id": order.client_id, "order_id": order.id, "topic": "checkPayment"}
        publish_event("checkPayment", message)

    def on_event(self, event):
        if event == 'Accepted':
            return orderAccepted(self.order)
        elif event == 'Declined':
            return returnResources(self.order)

        return self

class returnResources(State):
    """
    The state which indicates the order has been declined
    """
    def __init__(self, order):
        self.order = order
        return orderDeclined(self.order)


class orderDeclined(State):
    """
    The state which indicates the order has been declined
    """
    def __init__(self, order):
        self.order = order
        from . import Session
        session = Session()
        order.cambiar_estado(session, order.id, order.STATUS_DECLINED)



class orderAccepted(State):
    """
    The state which indicates the order has been accepted
    """
    def __init__(self, order):
        self.order = order
        from . import Session
        session = Session()
        order.cambiar_estado(session, order.id, order.STATUS_ACEPTED)
        message1 = {"order_id": order.id}
        publish_event("created", message1)
        for x in range(order.number_of_pieces):
            message2 = {"order_id": order.id, "number_of_pieces": 1}
            publish_event("piece", message2)

# End of our states.