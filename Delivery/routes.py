from flask import request, jsonify, abort
from flask import current_app as app
from .models import Delivery
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session
from .delivery import  view_delivery_by_id, view_all_deliveres, create_delivery_d, update_status_delivery

# Order Routes #########################################################################################################
@app.route('/delivery', methods=['POST'])
def create_delivery():
    session = Session()
    new_delivery = None
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
        content = request.json
        new_delivery = create_delivery_d(content['order_id'])
        response = jsonify(new_delivery.as_dict())
        session.close()
    else:
        responde = none
    return response


@app.route('/deliveries', methods=['GET'])
def view_deliveries():
    deliveries = view_deliveries()
    response = jsonify(Delivery.list_as_dict(deliveries))
    return response


# view one delivery
@app.route('/delivery/<int:id>', methods=['GET'])
def view_delivery(id):
    delivery = view_delivery_by_id(id)
    response = jsonify(delivery.as_dict())
    return response


@app.route('/delivery/<string:status>/<int:id>', methods=['PATCH'])
def update_status_sent(status, id):
    update_status_delivery(id, status)
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
