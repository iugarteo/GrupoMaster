from flask import request, jsonify, abort
from flask import current_app as app
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session, checkJWT
import psutil
import os
from sqlalchemy import create_engine
# Log Routes #######################################################################################################
from .logic import read_all_events, read_event_by_id
from .models import Event


@app.route('/log/<int:event_id>', methods=['GET'])
def view_event(event_id):
    token = request.headers["Authorization"].split(" ")
    permissions = checkJWT.checkPermissions("log.view_event", token[1])
    session = Session()
    if permissions:
        event = read_event_by_id(session, event_id)
        response = jsonify(event.as_dict())
    else:
        abort(BadRequest.code)
    if not event:
        abort(NotFound.code)
    session.close()
    return response


@app.route('/log', methods=['GET'])
def view_all_events():
    token = request.headers["Authorization"].split(" ")
    permissions = checkJWT.checkPermissions("log.view_all_events", token[1])
    session = Session()
    if permissions:
        events = read_all_events(session)
        response = jsonify(Event.list_as_dict(events))
    else:
        abort(BadRequest.code)
    session.close()
    return response

# Health Check ################
@app.route('/log/health', methods=['HEAD', 'GET'])
def health_check():
#abort(BadRequest)
	#if(machine.state == "Free"):
	    #messagge = "The service Order is up and free, give it some work."
	 #if(machine.state == "Working"):
	    #messagge = "The service Order is up but currently working, wait a little." 
	#if(machine.state == "Down"):
	    #messagge = "The machine is down, we are working on it."
	###Extra
	#fichero = os.path.exists("./public_key.pem")
	#if (fichero == True):
	#	testFich = "Existe una pubkey en este servicio"
	#else:
	#	testFich =  "No existe pubkey en este servicio"

	#cpuTest = psutil.cpu_percent(1)
	#ramTest = psutil.virtual_memory().percent
	#memTest = (psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

	#engineTest = create_engine(Config.SQLALCHEMY_DATABASE_URI) ##Supongo que este engine luego habria que cerrarlo, 
								## Lo unico encontrado es dispose(), pero no se si es eso
	#if(engineTest.connect()):
	#	conexionDB = "Es posible la conexión con la BD"
	#if(!engineTest.connect()):
	#	conexionDB = "No es posible la conexión con la BD"

	#response = jsonify(estado = messagge,
	#pubKey=testFich,
	#cpu=cpuTest,
	#ram= ramTest, 
	#mem = memTest,
	#db = conexionDB)

	#return response
	return "Ok"

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
