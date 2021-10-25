from flask import request, jsonify, abort
from flask import current_app as app
from .models import Order
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from .order import pedir_pago, realizar_pedido, llamar_delivery, cambiar_estado
from . import Session

# Order Routes #########################################################################################################
@app.route('/crear_order', methods=['POST'])
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
        session.commit()
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(new_order.as_dict())
    session.close()
    #LLamar a create Delivery
    return response


#@app.route('/order', methods=['GET'])
@app.route('/ver_order/<int:order_id>', methods=['GET'])
def getOrder(order_id):
    session = Session()
    order = session.query(Order).get(order_id)
    if not order:
        session.close()
        abort(NotFound.code)
    print("GET Order {}.".format(order_id))

    response = jsonify(order.as_dict())
    session.close()
    return response

@app.route('/ver_orders', methods=['GET'])
def view_orders():
    session = Session()
    print("GET All Orders.")
    orders = session.query(Order).all()
    response = jsonify(Order.list_as_dict(orders))
    session.close()
    return response


@app.route('/llamr_pedido/<int:order_id>', methods=['GET'])
def realizar_pedido_ruta(order_id):
    session = Session()
    order = session.query(Order).get(order_id)
    if not order:
        abort(NotFound.code)
    response = jsonify(order.as_dict())
    print("GET realizar_pedido_ruta {}.".format(order_id))
    string_resultado = realizar_pedido(order_id)
    print(string_resultado)
    session.close()
    return string_resultado

@app.route('/llamar_pago/<int:order_id>', methods=['GET'])
def pedir_pago_ruta(order_id):
    session = Session()
    order = session.query(Order).get(order_id)
    if not order:
        abort(NotFound.code)
    print("GET Order {}: {}".format(order_id, order))
    response = jsonify(order.as_dict())
    string_resultado = pedir_pago(order_id)
    session.close()
    return string_resultado


@app.route('/borrar_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    session = Session()
    order = session.query(Order).get(order_id)
    if not order:
        session.close()
        abort(NotFound.code)
    print("DELETE Order {}.".format(order_id))
    session.delete(order)
    session.commit()
    response = jsonify(order.as_dict())
    session.close()
    return response

#Cambiar estados
@app.route('/alterar_estado_order/<int:order_id>/<string:estado>', methods=['PATCH'])
def update_status(order_id, estado):
    session = Session()
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    try:
        print("order_id: ", order_id)
        order = cambiar_estado(session, order_id, estado)
        if(order != "No existe ese estado"):
            session.commit()
        else:
            print(order)
            abort(BadRequest.code)
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(order.as_dict())
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


