
from . import Session
from flask import request, jsonify, abort
from .models import Client, Role
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
from . import security



def registClient(content):

    session = Session()
    new_client = None
    pasEnc = security.hashPassword(content['password'])
    try:
        new_client = Client(
            name=content['name'],
            surname=content['surname'],
            password=pasEnc,
            nickname=content['nickname']
        )
        session.add(new_client)
        session.commit()
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(new_client.as_dict())
    session.close()
    return response

def getAllClients():
    session = Session()
    print("GET All Clients.")
    clients = session.query(Client).all()
    response = jsonify(Client.list_as_dict(clients))
    session.close()
    return response

def getClient(client_id):
    session = Session()
    client = session.query(Client).get(client_id)
    if not client:
        abort(NotFound.code)
    print("GET Client {}: {}".format(client_id, client))
    response = jsonify(client.as_dict())
    session.close()
    return response

def deleteClient(client_id):
    session = Session()
    client = session.query(Client).get(client_id)
    if not client:
        session.close()
        abort(NotFound.code)
    print("DELETE Client {}.".format(client_id))
    session.delete(client)
    session.commit()
    response = jsonify(client.as_dict())
    session.close()
    return response

def createRole(content):

    session = Session()
    new_role = None
    try:
        new_role = Role(
            name=content['name'],
            permisions=content['permisions']
        )
        session.add(new_role)
        session.commit()
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(new_role.as_dict())
    session.close()
    return response

def updateRole(id,content):
    session = Session()
    role = session.query(Role).get(id)
    try:
        role.name = content['name']
        role.permisions = content['permisions']
        session.commit()
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(role.as_dict())
    session.close()
    return response

def getAllRoles():
    session = Session()
    print("GET All Roles.")
    roles = session.query(Role).all()
    response = jsonify(Role.list_as_dict(roles))
    session.close()
    return response

def getRole(role_id):
    session = Session()
    role = session.query(Role).get(role_id)
    if not role:
        abort(NotFound.code)
    print("GET Role {}: {}".format(role_id, role))
    response = jsonify(role.as_dict())
    session.close()
    return response

def deleteRole(role_id):
    session = Session()
    role = session.query(Role).get(role_id)
    if not role:
        session.close()
        abort(NotFound.code)
    print("DELETE Role {}.".format(role_id))
    session.delete(role)
    session.commit()
    response = jsonify(role.as_dict())
    session.close()
    return response

def authentication(nickname, password):
    session = Session()
    client = session.query(Client).filter(Client.nickname==nickname).all()
    role = session.query(Role).filter(Role.id==client.role_id).all()
    if not client:
        session.close()
        abort(NotFound.code)
    auth = security.checkPass(password, client[0])
    session.close()
    if (auth == True):
        print("Authentication correct!")
        response = security.getToken(client, role)
    else:
        print("Authentication incorrect! ERROR!!!!!!")
        abort(BadRequest.code)
    return response

