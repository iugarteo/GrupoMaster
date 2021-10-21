from flask import request, jsonify, abort
from flask import current_app as app
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import logic
from . import security



# Client Routes #########################################################################################################
@app.route('/regist', methods=['POST'])
def create_client():

    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json

    response = logic.registClient(content)

    return response

@app.route('/auth', methods=['GET'])
def auth_client():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    response = logic.authentication(content['nickname'], content['password'])


    return response

@app.route('/pubKey', methods=['GET'])
def pub_key():

    response = security.getPublicKey()

    return response

@app.route('/clients', methods=['GET'])
def view_clients():
    response = logic.getAllClients()
    return response


@app.route('/client/<int:client_id>', methods=['GET'])
def view_client(client_id):
    response = logic.getClient(client_id)
    return response


@app.route('/client/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    response = logic.deleteClient(client_id)
    return response

#Role routes
@app.route('/role', methods=['POST'])
def create_Role():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    response = logic.createRole(content)
    return response

@app.route('/roles', methods=['GET'])
def view_roles():
    response = logic.getAllRoles()
    return response


@app.route('/role/<int:role_id>', methods=['GET'])
def view_role(role_id):
    response = logic.getRole(role_id)
    return response


@app.route('/role/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    response = logic.deleteRole(role_id)
    return response

@app.route('/roleUpdate/<int:role_id>', methods=['UPDATE'])
def create_Role(role_id):
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    response = logic.updateRole(role_id,content)
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


