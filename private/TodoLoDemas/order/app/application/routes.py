from flask import request, jsonify, abort
from flask import current_app as app
from .models import Order
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from .order import addPiece, pedir_pago, cambiar_estado, crear_order, ver_order_id, ver_orders, delete_order
from . import Session
from .checkJWT import checkPermissions

# Order Routes #########################################################################################################
@app.route('/order/crear_order', methods=['POST'])
def create_order():

    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    token = request.headers["Authorization"].split(" ")

    if checkPermissions("order.create_order", token[1]):
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

    token = request.headers["Authorization"].split(" ")

    if checkPermissions("order.ver_order", token[1]):
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

    token = request.headers["Authorization"].split(" ")

    if checkPermissions("order.ver_orders", token[1]):
        session = Session()
        orders = ver_orders(session)
        response = jsonify(Order.list_as_dict(orders))
        session.close()
        return response
    else:
        response = "Error - Token sin autorización"
        return response

@app.route('/order/addPiece/<int:order_id>', methods=['GET']) 
def addPiece(order_id):	
##Diria que no necesita permisos
    print("Add piece to Order ", order_id)
	
    addPiece(order_id)

    return "Piece added!"
    
@app.route('/order/borrar_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):

    token = request.headers["Authorization"].split(" ")

    if checkPermissions("order.borrar_order", token[1]):
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


@app.route('/order/anyadir_pieza/<int:order_id>', methods=['GET'])
def anyadir_pieza(order_id):
    ##Diria que no necesita permisos
    print("Add piece to Order ", order_id)
    session = Session()
    anyadirPieza(session, order_id)
    session.close()
    return "Pieces Added!"

#Cambiar estados
@app.route('/order/alterar_estado_order/<int:order_id>/<string:estado>', methods=['PATCH'])
def update_status(order_id, estado):

    token = request.headers["Authorization"].split(" ")

    if checkPermissions("order.alterar_estado_order", token[1]):
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
# Health Check ################

@app.route('/order/health', methods=['HEAD', 'GET'])
def health_check():
 #abort(BadRequest)
#if(machine.state == "Free"):
    #return "The service Order is up and free, give it some work."
 #if(machine.state == "Working"):
    #return "The service Order is up but currently working, wait a little." 
#if(machine.state == "Down"):
    #return "The machine is down, we are working on it."
 return "OK"

# Errores ###############
def get_jsonified_error(e):
    traceback.print_tb(e.__traceback__)
    return jsonify({"error_code":e.code, "error_message": e.description}), e.code


