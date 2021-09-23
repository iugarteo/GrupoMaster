from flask import request, jsonify, abort
from flask import current_app as app
from .models import Delivery
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session


# Order Routes #########################################################################################################
@app.route('/delivery', methods=['POST'])
def create_delivery():
    session = Session()
    new_delivery = None
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    try:
        new_delivery = Delivery(
            order_id=content['order_id'],
            status=Delivery.STATUS_WORKING
        )
        session.add(new_delivery)
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(new_delivery.as_dict())
    session.close()
    return response


@app.route('/deliveries', methods=['GET'])
def view_deliveries():
    session = Session()
    print("GET All Orders.")
    orders = session.query(Delivery).all()
    response = jsonify(Delivery.list_as_dict(orders))
    session.close()
    return response


# view one delivery
@app.route('/delivery/<int:id>', methods=['GET'])
def view_delivery(id):
    session = Session()
    delivery = session.query(Delivery).get(id)
    if not delivery:
        abort(NotFound.code)
    print("GET Order {}: {}".format(id, delivery))
    response = jsonify(delivery.as_dict())
    session.close()
    return response


@app.route('/delivery/send/<int:id>', methods=['PATCH'])
def update_status_sent(id):
    session = Session()
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
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

@app.route('/delivery/received/<int:id>', methods=['PATCH'])
def update_status_received(id):
    session = Session()
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
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

# Error Handling #######################################################################################################
@app.errorhandler(UnsupportedMediaType)
def unsupported_media_type_handler(e):
    return get_jsonified_error(e)


@app.errorhandler(BadRequest)
def bad_request_handler(e):
    return get_jsonified_error(e)


@app.errorhandler(NotFound)
def resource_not_found_handler(e):
    return get_jsonified_error(e)


@app.errorhandler(InternalServerError)
def server_error_handler(e):
    return get_jsonified_error(e)


def get_jsonified_error(e):
    traceback.print_tb(e.__traceback__)
    return jsonify({"error_code": e.code, "error_message": e.description}), e.code
