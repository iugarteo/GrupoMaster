from .models import Delivery


def view_delivery_by_id(session, delivery_id):
    delivery = session.query(Delivery).get(delivery_id)
    if not delivery:
        session.close()
        return None
    print("GET Delivery {}: {}".format(delivery_id, delivery))
    return delivery

def view_all_deliveres(session):
    print("GET All Deliveries")
    deliveries = session.query(Delivery).all()
    return deliveries

def update_status_delivery(sesssion, delivery_id, status):
    session = Session()
    delivery = session.query(Delivery).get(delivery_id)
    delivery.status = Delivery.status
    print("Updated Delivery {} status: {}".format(delivery_id,delivery.status))
    session.commit()
    session.rollback()
    session.close()

def create_delivery_d(session, order_id):
    session = Session()
    new_delivery = None
    try:
        new_delivery = Delivery(
            order_id=order_id,
            status=Delivery.STATUS_WORKING
        )
        session.add(new_delivery)
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
    return new_delivery
