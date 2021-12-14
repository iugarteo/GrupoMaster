from .state import State
from .publisher import publish_event
from . import order

# Start of our states
class deliveryChecking(State):
    """
    The state which indicates order is checking the delivery address
    """
    def __init__(self, orderObject):
        self.order = orderObject
        from . import Session
        session = Session()
        order.cambiar_estado(session, orderObject.id, orderObject.STATUS_PENDING_DELIVERY)
        print('Processing current state:', str(self))
        message = {"orderId": orderObject.id, "zipCode": orderObject.zip_code, "topic": "checkAddress"}
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
    def __init__(self, orderObject):
        self.order = orderObject
        from . import Session
        session = Session()
        order.cambiar_estado(session, orderObject.id, orderObject.STATUS_PENDING_ON_PAYMENT)
        print('Processing current state:', str(self))
        precio = orderObject.price_total
        message = {"price": precio, "client_id": orderObject.client_id, "order_id": orderObject.id, "topic": "checkPayment"}
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
    def __init__(self, orderObject):
        self.order = orderObject
        return orderDeclined(self.order)


class orderDeclined(State):
    """
    The state which indicates the order has been declined
    """
    def __init__(self, orderObject):
        self.order = orderObject
        from . import Session
        session = Session()
        order.cambiar_estado(session, orderObject.id, orderObject.STATUS_DECLINED)



class orderAccepted(State):
    """
    The state which indicates the order has been accepted
    """
    def __init__(self, orderObject):
        self.order = orderObject
        from . import Session
        session = Session()
        order.cambiar_estado(session, orderObject.id, orderObject.STATUS_ACEPTED)
        message1 = {"order_id": orderObject.id}
        publish_event("created", message1)
        for x in range(orderObject.number_of_pieces):
            message2 = {"order_id": orderObject.id, "number_of_pieces": 1}
            publish_event("piece", message2)

# End of our states.