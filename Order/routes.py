from flask import request, jsonify, abort
from flask import current_app as app
from .models import Order, Piece
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from .machine import Machine
from . import Session

my_order = Order()

# Order Routes #########################################################################################################
@app.route('/order', methods=['POST'])
def create_order():
    session = Session()
    new_order = None
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    try:
        new_order = Order(
            description=content['description'],
            number_of_pieces=content['number_of_pieces'],
            status=Order.STATUS_CREATED
        )
        session.add(new_order)
        for i in range(new_order.number_of_pieces):
            piece = Piece()
            piece.order = new_order
            session.add(piece)
        session.commit()
        my_machine.add_pieces_to_queue(new_order.pieces)
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(new_order.as_dict())
    session.close()
    return response


@app.route('/order', methods=['GET'])
@app.route('/orders', methods=['GET'])
def view_orders():
    session = Session()
    print("GET All Orders.")
    orders = session.query(Order).all()
    response = jsonify(Order.list_as_dict(orders))
    session.close()
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
    order = session.query(Order).get(order_id)
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
@app.route('/order/finish/<int:id>', methods=['PATCH'])
def update_status_finish(id):
    session = Session()
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    try:
        order= session.query(Order).get(id)
        order.status = Order.STATUS_FINISHED
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(order.as_dict())
    my_order.llamar_delivery()
    session.close()
    return response

@app.route('/order/declined/<int:id>', methods=['PATCH'])
def update_status_decline(id):
    session = Session()
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    try:
        order= session.query(Order).get(id)
        order.status = Order.STATUS_DECLINED
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(order.as_dict())
    return response


# Piece Routes #########################################################################################################

@app.route('/piece', methods=['GET'])
@app.route('/pieces', methods=['GET'])
def view_pieces():
    session = Session()
    order_id = request.args.get('order_id')
    if order_id:
        pieces = session.query(Piece).filter_by(order_id=order_id).all()
    else:
        pieces = session.query(Piece).all()
    response = jsonify(Piece.list_as_dict(pieces))
    session.close()
    return response


@app.route('/piece/<int:piece_ref>', methods=['GET'])
def view_piece(piece_ref):
    session = Session()
    piece = session.query(Piece).get(piece_ref)
    if not piece:
        session.close()
        abort(NotFound.code)
    print(piece)
    response = jsonify(piece.as_dict())
    session.close()
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


