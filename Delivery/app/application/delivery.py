from . import Session
from flask import request, jsonify, abort
from .models import Delivery
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType

def registDelivery(content):
    session = Session()
    new_delivery = None
    try:
        new_delivery = Delivery(
            order_id=content['order_id'],
            status=Delivery.STATUS_WORKING
        )
        session.add(new_delivery)
        session.commit()
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(new_delivery.as_dict())
    session.close()
    return response

def getAllDeliveries():
    session = Session()
    print("GET All Deliveries.")
    deliveries = session.query(Delivery).all()
    response = jsonify(Delivery.list_as_dict(deliveries))
    session.close()
    return response

def getDelivery(delivery_id):
    session = Session()
    delivery = session.query(Delivery).get(delivery_id)
    if not delivery:
        abort(NotFound.code)
    print("GET Delivery {}: {}".format(delivery_id, delivery))
    response = jsonify(delivery.as_dict())
    session.close()
    return response

def deleteDelivery(delivery_id):
    session = Session()
    delivery = session.query(Delivery).get(delivery_id)
    if not delivery:
        session.close()
        abort(NotFound.code)
    print("DELETE Delivery {}.".format(delivery_id))
    session.delete(delivery)
    session.commit()
    response = jsonify(delivery.as_dict())
    session.close()
    return response

def deliverySent(id):
    session = Session()
    try:
        delivery = session.query(Delivery).get(id)
        delivery.status = Delivery.STATUS_SENT
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(delivery.as_dict())
    session.close()
    return response

def deliveryReceived(id):
    session = Session()
    try:
        delivery = session.query(Delivery).get(id)
        delivery.status = Delivery.STATUS_RECEIVED
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(delivery.as_dict())
    session.close()
    return response
