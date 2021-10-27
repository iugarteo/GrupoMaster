from flask import request, jsonify, abort
from flask import current_app as app
from .models import Delivery
from . import delivery, checkJWT
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session


# Delivery Routes #########################################################################################################
@app.route('/delivery/create', methods=['POST'])
def create_delivery():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    token = request.headers["token"]
    permisions = checkJWT.checkPermissions("delivery.create", token)
    if permisions == True:
        session = Session()
        response = delivery.registDelivery(session, content)
        session.close()
    else:
        abort(BadRequest.code)
    return response


@app.route('/delivery/deliveries', methods=['GET'])
def view_deliveries():
    token = request.headers["token"]
    permisions = checkJWT.checkPermissions("delivery.deliveries", token)
    if permisions == True:
        session = Session()
        response = delivery.getAllDeliveries(session)
        session.close()
    else:
        abort(BadRequest.code)
    return response


# view one delivery
@app.route('/delivery/getDelivery/<int:id>', methods=['GET'])
def view_delivery(id):
    token = request.headers["token"]
    permisions = checkJWT.checkPermissions("delivery.getDelivery", token)
    if permisions == True:
        session = Session()
        response = delivery.getDelivery(session, id)
        session.close()
    else:
        abort(BadRequest.code)
    return response

@app.route('/delivery/send/<int:id>', methods=['PATCH'])
def update_status_sent(id):
    token = request.headers["token"]
    permisions = checkJWT.checkPermissions("delivery.send", token)
    if permisions == True:
        session = Session()
        response = delivery.deliverySent(session, id)
        session.close()
    else:
        abort(BadRequest.code)
    return response

@app.route('/delivery/received/<int:id>', methods=['PATCH'])
def update_status_received(id):
    token = request.headers["token"]
    permisions = checkJWT.checkPermissions("delivery.received", token)
    if permisions == True:
        session = Session()
        response = delivery.deliveryReceived(id)
        session.close()
    else:
        abort(BadRequest.code)
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