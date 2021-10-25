from flask import request, jsonify, abort
from flask import current_app as app
from .models import Delivery
from . import delivery
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session


# Order Routes #########################################################################################################
@app.route('/create_delivery', methods=['POST'])
def create_delivery():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    response = delivery.registDelivery(content)
    return response


@app.route('/deliveries', methods=['GET'])
def view_deliveries():
    response = delivery.getAllDeliveries()
    return response


# view one delivery
@app.route('/delivery/<int:id>', methods=['GET'])
def view_delivery(id):
    response = delivery.getDelivery(id)
    return response

@app.route('/delivery_send/<int:id>', methods=['PATCH'])
def update_status_sent(id):
    response = delivery.deliverySent(id)
    return response

@app.route('/delivery_received/<int:id>', methods=['PATCH'])
def update_status_received(id):
    response = delivery.deliveryReceived(id)
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