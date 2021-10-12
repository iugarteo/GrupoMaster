from .models import Order, Piece


def view_order_by_id(session, order_id):
    order = session.query(Order).get(order_id)
    if not order:
        session.close()
        return None
    print("GET Order {}: {}".format(order_id, order))
    return order

def view_all_orders(session):
    print("GET All Orders")
    orders = session.query(Order).all()
    return orders

def update_status_order(sesssion, order_id, status):
    session = Session()
    order = session.query(Order).get(order_id)
    order.status = Order.status
    print("Updated Order {} status: {}".format(order_is,order.status))
    session.commit()
    session.rollback()
    session.close()

def create_order_d(session, pieces_id, description, num_pieces):
    session = Session()
    new_order = None
    try:
        new_order = Order(
            pieces=pieces_id,
            description=description,
            num_pieces=num_pieces
        )
        session.add(new_order)
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
    return new_order
