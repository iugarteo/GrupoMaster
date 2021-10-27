from flask import request, jsonify, abort
from flask import current_app as app
from .models import Order
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from .order import realizar_pedido, cambiar_estado, crear_order, ver_order_id, ver_orders, delete_order
from . import Session
from .checkJWT import checkPermissions

# Order Routes #########################################################################################################
@app.route('/order/crear_order', methods=['POST'])
def create_order():

    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)

    content = request.json
    token = request.headers['token']

    if checkPermissions("order.create_order", token):
        session = Session()
        new_order = crear_order(session,content)
        response = jsonify(new_order.as_dict())
        #LLamar a create Delivery
        session.close()
        return response
    else:
        response = "Error - Token sin autorización"
        return response


#@app.route('/order', methods=['GET'])
@app.route('/order/ver_order/<int:order_id>', methods=['GET'])
def getOrder(order_id):

    #if request.headers['Content-Type'] != 'application/json':
    #    abort(UnsupportedMediaType.code)

    token = request.headers['token']

    if checkPermissions("order.ver_order", token):
        session = Session()
        order = ver_order_id(session, order_id)
        if not order:
            session.close()
            abort(NotFound.code)
        print("GET Order {}.".format(order_id))
        response = jsonify(order.as_dict())
        # LLamar a create Delivery
        session.close()
        return response
    else:
        response = "Error - Token sin autorización"
        return response

@app.route('/order/ver_orders', methods=['GET'])
def view_orders():

    print("GET All Orders.")

    token = request.headers['token']

    if checkPermissions("order.ver_orders", token):
        session = Session()
        orders = ver_orders(session)
        response = jsonify(Order.list_as_dict(orders))
        session.close()
        return response
    else:
        response = "Error - Token sin autorización"
        return response

@app.route('/order/borrar_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):

    token = request.headers['token']

    if checkPermissions("order.borrar_order", token):
        session = Session()
        order = session.query(Order).get(order_id)
        if not order:
            session.close()
            abort(NotFound.code)
        print("DELETED Order {}.".format(order_id))
        response = jsonify(order.as_dict())
        session.close()
        return response

    else:
        response = "Error - Token sin autorización"
        return response

#Cambiar estados
@app.route('/order/alterar_estado_order/<int:order_id>/<string:estado>', methods=['PATCH'])
def update_status(order_id, estado):

    token = request.headers['token']

    if checkPermissions("order.alterar_estado_order", token):
        session = Session()
        try:
            print("order_id: ", order_id)
            order = cambiar_estado(session, order_id, estado)
            if(order != "No existe ese estado"):
                session.commit()
                response = jsonify(order.as_dict())
            else:
                print(order)
                abort(BadRequest.code)
        except KeyError:
            session.rollback()
            abort(BadRequest.code)

        session.close()
        return response

    else:
        response = "Error - Token sin autorización"
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


