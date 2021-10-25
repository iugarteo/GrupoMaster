from flask import request, jsonify, abort
from flask import current_app as app
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import logic
from . import security


# Client Routes #########################################################################################################
@app.route('/client/regist', methods=['POST'])
def create_client():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json

    response = logic.registClient(content)

    return response


@app.route('/client/auth', methods=['GET'])
def auth_client():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    jwt, refresh_token = logic.authentication(content['nickname'], content['password'])
    response = jsonify(jwt, refresh_token)
    return response

@app.route('/client/newJWT', methods=['GET'])
def new_jwt():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    response = logic.newJWT(content['refresh_token'], content['nickname'])
    return response

@app.route('/client/clients', methods=['GET'])
def view_clients():
    response = logic.getAllClients()
    return response


@app.route('/client/getclient/<int:client_id>', methods=['GET'])
def view_client(client_id):
    response = logic.getClient(client_id)
    return response


@app.route('/client/deleteclient/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    response = logic.deleteClient(client_id)
    return response


# Key routes
@app.route('/client/pubKey', methods=['GET'])
def pub_key():
    response = security.getPublicKey()

    return response


@app.route('/client/refreshKeys', methods=['GET'])
def refresh_key():
    token = request.headers["token"]
    admin = logic.checkPermissions("client.refresh", token)
    if admin == True:
        security.genKeys()
        response = security.getPublicKey()
    else:
        abort(BadRequest.code)
    return response


# Role routes
@app.route('/client/role', methods=['POST'])
def create_Role():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    response = logic.createRole(content)
    return response


@app.route('/client/roles', methods=['GET'])
def view_roles():
    response = logic.getAllRoles()
    return response


@app.route('/client/getrole/<int:role_id>', methods=['GET'])
def view_role(role_id):
    response = logic.getRole(role_id)
    return response


@app.route('/client/deleterole/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    response = logic.deleteRole(role_id)
    return response


@app.route('/client/roleUpdate/<int:role_id>', methods=['PATCH'])
def update_Role(role_id):
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    response = logic.updateRole(role_id, content)
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
