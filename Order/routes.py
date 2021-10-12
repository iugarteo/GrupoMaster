from flask import request, jsonify, abort
from flask import current_app as app
from .models import Order, Piece
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from .machine import Machine
from . import Session
from .order import view_order_by_id, view_all_orders, update_status_order, create_order_d

# Order Routes #########################################################################################################
@app.route('/order', methods=['POST'])
def create_order():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
        content = request.json
        new_order = create_order_d(content['pieces_id'],content['description'],content['num_pieces'])
        response = jsonify(new_order.as_dict())
        session.close()
    else:
        response = none
    return response


@app.route('/order', methods=['GET'])
@app.route('/orders', methods=['GET'])
def view_orders():
    orders = view_all_orders()
    response = jsonify(Order.list_as_dict(orders))
    return response


@app.route('/order/realizar_pedido/<int:order_id>', methods=['POST'])
def realizar_pedido_ruta(order_id):
    session = Session()
    order = session.query(Order).get(order_id)
    if not order:
        abort(NotFound.code)
    response = jsonify(order.as_dict())
    my_order.realizar_pedido(order_id)
    session.close()
    return response

@app.route('/order/pedirPago/<int:order_id>', methods=['GET'])
def pedir_pago_ruta(order_id):
    session = Session()
    order = session.query(Order).get(order_id)
    if not order:
        abort(NotFound.code)
    print("GET Order {}: {}".format(order_id, order))
    response = jsonify(order.as_dict())
    my_order.pedir_pago(order_id)
    session.close()
    return response

@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    session = Session()
    order = view_order_by_id(order_id)
    if not order:
        session.close()
        abort(NotFound.code)
    print("DELETE Order {}.".format(order_id))
    my_machine.remove_pieces_from_queue(order.pieces)
    session.delete(order)
    session.commit()
    response = jsonify(order.as_dict())
    session.close()
    return response

#Cambiar estados
@app.route('/order/<string:status>/<int:id>', methods=['PATCH'])
def update_status(status, id):
    order = update_status_order(id, status)
    response = jsonify(order.as_dict())
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
    return jsonify({"error_code":e.code, "error_message": e.description}), e.code


