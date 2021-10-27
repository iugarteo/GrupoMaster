from flask import request, jsonify, abort
from flask import current_app as app
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session, checkJWT

# Log Routes #######################################################################################################
from .logic import read_all_events, read_event_by_id
from .models import Event


@app.route('/log/<int:event_id>', methods=['GET'])
def view_payment(event_id):
    session = Session()
    #token = request.headers["token"]
    #permissions = checkJWT.checkPermissions("payment.getPayments", token)
    #if permissions == True:
    event = read_event_by_id(session, event_id)
    response = jsonify(event.as_dict())
    #else:
    #    abort(BadRequest.code)
    if not event:
        abort(NotFound.code)
    session.close()
    return response

@app.route('/log', methods=['GET'])
def view_all_logs():
    session = Session()
    #token = request.headers["token"]
    #permissions = checkJWT.checkPermissions("payment.getPayments", token)
    #if permissions:
    events = read_all_events(session)
    response = jsonify(Event.list_as_dict(events))
    #else:
    #    abort(BadRequest.code)
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
    return jsonify({"error_code": e.code, "error_message": e.description}), e.code
