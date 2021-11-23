from flask import request, jsonify, abort
from .models import Delivery
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType


def registDelivery(session, content):
    new_delivery = None
    try:
        new_delivery = Delivery(
            order_id=content['order_id'],
            status=Delivery.STATUS_WORKING
        )
        session.add(new_delivery)
        session.commit()
    except KeyError:
        session.rollback()
        abort(BadRequest.code)
    response = jsonify(new_delivery.as_dict())
    return response


def create_delivery(session, order_id):
    try:
        new_delivery = Delivery(
            order_id=order_id,
            status=Delivery.STATUS_WORKING
        )
        session.add(new_delivery)
        session.commit()
    except KeyError:
        session.rollback()
        new_delivery = None
    return new_delivery


def getAllDeliveries(session):
    print("GET All Deliveries.")
    deliveries = session.query(Delivery).all()
    response = jsonify(Delivery.list_as_dict(deliveries))
    return response


def getDelivery(session, delivery_id):
    delivery = session.query(Delivery).get(delivery_id)
    if not delivery:
        abort(NotFound.code)
    print("GET Delivery {}: {}".format(delivery_id, delivery))
    response = jsonify(delivery.as_dict())
    return response


def update_delivery_by_order(session, order_id, status):
    delivery = session.query(Delivery).filter_by(order_id=order_id).first()
    if not delivery:
        return None
    try:
        delivery.status = status
        session.commit()
    except KeyError:
        session.rollback()
    return delivery


def deleteDelivery(session, delivery_id):
    delivery = session.query(Delivery).get(delivery_id)
    if not delivery:
        session.close()
        abort(NotFound.code)
    print("DELETE Delivery {}.".format(delivery_id))
    session.delete(delivery)
    session.commit()
    response = jsonify(delivery.as_dict())
    return response

def deliverySent(session, id):
    try:
        delivery = session.query(Delivery).get(id)
        delivery.status = Delivery.STATUS_SENT
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(delivery.as_dict())
    return response

def deliveryReceived(session, id):
    try:
        delivery = session.query(Delivery).get(id)
        delivery.status = Delivery.STATUS_RECEIVED
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(delivery.as_dict())
    return response
