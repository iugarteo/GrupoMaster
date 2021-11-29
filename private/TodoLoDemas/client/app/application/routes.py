from flask import request, jsonify, abort
from flask import current_app as app
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
import traceback
from . import logic, Session
from . import security
import base64


# Client Routes #########################################################################################################
@app.route('/client/regist', methods=['POST'])
def create_client():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    #token = request.headers["token"]
    #permisions = logic.checkPermissions("client.regist", token)
    #if permisions == True:
    session = Session()
    response = logic.registClient(content, session)
    #else:
    #    abort(BadRequest.code)


    return response


@app.route('/client/auth', methods=['GET'])
def auth_client():
    session = Session()
    cuenta = request.headers["Authorization"].split(" ")
    base64_bytes = cuenta[1].encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    username, password = message.split(":", 1)

    response = logic.authentication(username, password, session)
    return response

@app.route('/client/newJWT', methods=['GET'])
def new_jwt():
    session = Session()
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    refreshToken=token = request.headers["Authorization"].split(" ")
    response = logic.newJWT(refreshToken[1], content['nickname'], session)
    return jsonify(newJWT=response)

@app.route('/client/clients', methods=['GET'])
def view_clients():
    token = request.headers["Authorization"].split(" ")
    permisions = logic.checkPermissions("client.clients", token[1])
    if permisions == True:
        session = Session()
        response = logic.getAllClients(session)
    else:
        abort(BadRequest.code)

    return response


@app.route('/client/getClient/<int:client_id>', methods=['GET'])
def view_client(client_id):
    token = request.headers["Authorization"].split(" ")
    permisions = logic.checkPermissions("client.getClient", token[1])
    if permisions == True:
        session = Session()
        response = logic.getClient(client_id,session)

    else:
        abort(BadRequest.code)
    return response


@app.route('/client/deleteClient/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    token = request.headers["Authorization"].split(" ")
    permisions = logic.checkPermissions("client.deleteClient", token[1])
    if permisions == True:
        session = Session()
        response = logic.deleteClient(client_id,session)
    else:
        abort(BadRequest.code)

    return response


# Key routes
@app.route('/client/pubKey', methods=['GET'])
def pub_key():
  
    response = security.getPublicKey()

    return response


@app.route('/client/refreshKeys', methods=['GET'])
def refresh_key():
    token = request.headers["Authorization"].split(" ")
    permisions = logic.checkPermissions("client.refresh", token[1])
    if permisions == True:
        response=logic.refreshKeys()

    else:
        abort(BadRequest.code)
    return response


# Role routes
@app.route('/client/role', methods=['POST'])
def create_Role():
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    #token = request.headers["token"]
    #permisions = logic.checkPermissions("client.role", token)
    #if permisions == True:
    session = Session()
    response = logic.createRole(content, session)
    #else:
    #    abort(BadRequest.code)

    return response


@app.route('/client/roles', methods=['GET'])
def view_roles():
    token = request.headers["Authorization"].split(" ")
    permisions = logic.checkPermissions("client.roles", token[1])
    if permisions == True:
        session = Session()
        response = logic.getAllRoles(session)
    else:
        abort(BadRequest.code)

    return response


@app.route('/client/getRole/<int:role_id>', methods=['GET'])
def view_role(role_id):
    token = request.headers["Authorization"].split(" ")
    permisions = logic.checkPermissions("client.getRole", token[1])
    if permisions == True:
        session = Session()
        response = logic.getRole(role_id, session)
    else:
        abort(BadRequest.code)

    return response


@app.route('/client/deleteRole/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    token = request.headers["Authorization"].split(" ")
    permisions = logic.checkPermissions("client.deleteRole", token[1])
    if permisions == True:
        session = Session()
        response = logic.deleteRole(role_id, session)
    else:
        abort(BadRequest.code)

    return response


@app.route('/client/roleUpdate/<int:role_id>', methods=['PATCH'])
def update_Role(role_id):
    if request.headers['Content-Type'] != 'application/json':
        abort(UnsupportedMediaType.code)
    content = request.json
    token = request.headers["Authorization"].split(" ")
    permisions = logic.checkPermissions("client.roleUpdate", token[1])
    if permisions == True:
        session = Session()
        response = logic.updateRole(role_id, content, session)
    else:
        abort(BadRequest.code)
    return response

# Health Check ################

@app.route('/health', methods=['HEAD', 'GET'])
def health_check():
 #abort(BadRequest)
 return "OK"

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
