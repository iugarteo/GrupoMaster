from flask import request, jsonify, abort
from flask import current_app as app
from .models import Delivery
from . import delivery, checkJWT
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session
import psutil
import os
from sqlalchemy import create_engine


# Delivery Routes #########################################################################################################
@app.route('/delivery/create', methods=['POST'])
def create_delivery():
    token = request.headers["Authorization"].split(" ")
    permisions = checkJWT.checkPermissions("delivery.create", token[1])
    #checkJWT.checkZIP(token[1])	
    if permisions == True:
        session = Session()
        response = delivery.registDelivery(session, content)
        session.close()
    else:
        abort(BadRequest.code)
    return response


@app.route('/delivery/deliveries', methods=['GET'])
def view_deliveries():
    token = request.headers["Authorization"].split(" ")
    permisions = checkJWT.checkPermissions("delivery.deliveries", token[1])
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
    token = request.headers["Authorization"].split(" ")
    permisions = checkJWT.checkPermissions("delivery.getDelivery", token[1])
    if permisions == True:
        session = Session()
        response = delivery.getDelivery(session, id)
        session.close()
    else:
        abort(BadRequest.code)
    return response

@app.route('/delivery/send/<int:id>', methods=['PATCH'])
def update_status_sent(id):
    token = request.headers["Authorization"].split(" ")
    permisions = checkJWT.checkPermissions("delivery.send", token[1])
    if permisions == True:
        session = Session()
        response = delivery.deliverySent(session, id)
        session.close()
    else:
        abort(BadRequest.code)
    return response

@app.route('/delivery/received/<int:id>', methods=['PATCH'])
def update_status_received(id):
    token = request.headers["Authorization"].split(" ")
    permisions = checkJWT.checkPermissions("delivery.received", token[1])
    if permisions == True:
        session = Session()
        response = delivery.deliveryReceived(id)
        session.close()
    else:
        abort(BadRequest.code)
    return response

# Health Check ################

@app.route('/delivery/health', methods=['HEAD', 'GET'])
def health_check():
 #abort(BadRequest)
	#if(machine.state == "Free"):
	    #messagge = "The service Order is up and free, give it some work."
	 #if(machine.state == "Working"):
	    #messagge = "The service Order is up but currently working, wait a little." 
	#if(machine.state == "Down"):
	    #messagge = "The machine is down, we are working on it."
	###Extra
	fichero = os.path.exists("./public_key.pem")
	if (fichero == True):
		testFich = "Existe una pubkey en este servicio"
	else:
		testFich =  "No existe pubkey en este servicio"

	cpuTest = psutil.cpu_percent(1)
	ramTest = psutil.virtual_memory().percent
	memTest = (psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

	engineTest = create_engine(Config.SQLALCHEMY_DATABASE_URI) ##Supongo que este engine luego habria que cerrarlo, 
								## Lo unico encontrado es dispose(), pero no se si es eso
	if(engineTest.connect()):
		conexionDB = "Es posible la conexión con la BD"
	if(engineTest.connect() == False):
		conexionDB = "No es posible la conexión con la BD"

	response = jsonify(#estado = messagge,
	pubKey=testFich,
	cpu=cpuTest,
	ram= ramTest, 
	mem = memTest,
	db = conexionDB)

	return response
	#return "Ok"

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
