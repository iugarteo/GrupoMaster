from flask import request, jsonify, abort
from flask import current_app as app
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session, checkJWT
import psutil
import os

# Log Routes #######################################################################################################
from .logic import read_all_logs, read_log_by_id
from .models import Log


@app.route('/logger/<int:event_id>', methods=['GET'])
def view_log(event_id):
    token = request.headers["Authorization"].split(" ")
    permissions = checkJWT.checkPermissions("logger.view_log", token[1])
    session = Session()
    if permissions:
        log = read_log_by_id(session, event_id)
        response = jsonify(log.as_dict())
    else:
        abort(BadRequest.code)
    if not log:
        abort(NotFound.code)
    session.close()
    return response


@app.route('/logger', methods=['GET'])
def view_all_logs():
    token = request.headers["Authorization"].split(" ")
    permissions = checkJWT.checkPermissions("logger.view_all_logs", token[1])
    session = Session()
    if permissions:
        events = read_all_logs(session)
        response = jsonify(Log.list_as_dict(events))
    else:
        abort(BadRequest.code)
    session.close()
    return response

# Health Check ################
@app.route('/logger/health', methods=['HEAD', 'GET'])
def health_check():
    fichero = os.path.exists("./public_key.pem")
    cpuTest = psutil.cpu_percent(1)
    ramTest = psutil.virtual_memory().percent
    if(fichero == True and cpuTest <= 50 and ramTest <= 50):
        return "Ok"
    else:
        abort(BadRequest.code)

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
