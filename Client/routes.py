from flask import request, jsonify, abort
from flask import current_app as app
from .models import Client
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import Session
from .client import view_client_by_id, view_all_clients, create_client

# Client Routes #########################################################################################################
@app.route('/client', methods=['POST'])
def create_client():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
        content = request.json
        new_client= create_client(content['name'],content['surname'])
        response = jsonify(new_client.as_dict())
    else:
        response = none
    return response


@app.route('/client', methods=['GET'])
@app.route('/clients', methods=['GET'])
def view_clients():
    clients = view_all_clients()
    response = jsonify(Client.list_as_dict(clients))
    return response


@app.route('/client/<int:client_id>', methods=['GET'])
def view_client(client_id):
    client = view_client_by_id(client_id)
    response = jsonify(client.as_dict())
    return response


@app.route('/client/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    session = Session()
    client = view_client_by_id(client_id)
    if not client:
        session.close()
        abort(NotFound.code)
    print("DELETE Client {}.".format(client_id))
    session.delete(client)
    session.commit()
    response = jsonify(client.as_dict())
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


