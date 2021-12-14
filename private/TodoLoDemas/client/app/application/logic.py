import logging

from flask import jsonify, abort

from .models import Client, Role
from werkzeug.exceptions import NotFound, BadRequest, Forbidden
from . import security
from . import publisher
import json

from .LoggingHandler import LoggingHandler


# logging.basicConfig(level=logging.DEBUG) Enables Debug and Info logs
logger = logging.getLogger('client')
handler = LoggingHandler()
logger.addHandler(handler)


def registClient(content, session):
    new_client = None
    pasEnc = security.hashPassword(content['password'])
    try:
        new_client = Client(
            name=content['name'],
            surname=content['surname'],
            password=pasEnc,
            nickname=content['nickname'],
            role_id=content['role_id'],
            zip_code=content['zip_code']
        )
        session.add(new_client)
        session.commit()
    except Exception as e:
        session.rollback()
        session.close()
        logger.warning(e)
        abort(BadRequest.code)
    response = jsonify(new_client.as_dict())
    session.close()
    return response

def getAllClients(session):
    logger.info("GET All Clients")
    clients = session.query(Client).all()
    response = jsonify(Client.list_as_dict(clients))
    session.close()
    return response

def getClient(client_id, session):
    client = session.query(Client).get(client_id)
    if not client:
        logger.info("GET Client {}: {}".format(client_id, client))
    response = jsonify(client.as_dict())
    session.close()
    return response

def deleteClient(client_id, session):
    client = session.query(Client).get(client_id)
    if not client:
        session.close()
        abort(NotFound.code, "Client not found")
    logger.info("DELETE Client {}.".format(client_id))
    session.delete(client)
    session.commit()
    response = jsonify(client.as_dict())
    session.close()
    return response

def createRole(content, session):

    new_role = None
    try:
        new_role = Role(
            name=content['name'],
            permissions=content['permissions']
        )
        session.add(new_role)
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    response = jsonify(new_role.as_dict())
    session.close()
    return response

def updateRole(id,content, session):
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

def getAllRoles(session):
    logger.info("GET All Roles.")
    roles = session.query(Role).all()
    response = jsonify(Role.list_as_dict(roles))
    session.close()
    return response

def getRole(role_id, session):
    role = session.query(Role).get(role_id)
    if not role:
        abort(NotFound.code)
    logger.info("GET Role {}: {}".format(role_id, role))
    response = jsonify(role.as_dict())
    session.close()
    return response

def deleteRole(role_id, session):
    role = session.query(Role).get(role_id)
    if not role:
        session.close()
        abort(NotFound.code)
    logger.info("DELETE Role {}.".format(role_id))
    session.delete(role)
    session.commit()
    response = jsonify(role.as_dict())
    session.close()
    return response


def authentication(nickname, password, session):
    client = session.query(Client).filter(Client.nickname==nickname).all()
    role = session.query(Role).filter(Role.id==client[0].role_id).all()
    if not client:
        session.close()
        abort(NotFound.code, f"Client {nickname} not found")
    if not role:
        session.close()
        abort(NotFound.code, f"Client's role not found ({role})")
    auth = security.checkPass(password, client[0])
    if auth:
        logger.info("Authentication correct %s", nickname)
        jwt = security.getToken(client[0], role[0])
        client[0].refresh_token = security.getRefreshToken()
        refresh_token = client[0].refresh_token
        session.commit()
        session.close()
    else:
        session.commit()
        session.close()
        logger.warning("Authentication incorrect! ERROR!!!!!!")
        abort(BadRequest.code)
    message = {"jwt":jwt, "refresh_token":refresh_token}
    return json.dumps(message)


def checkPermissions(permision, token):
    decoded = security.readToken(token, security.getPublicKey())
    if decoded == None:
        return False
    else:
        permisions = decoded["Permisions"].split(",")
    if permision in permisions:
        boolean = True
    else:
        boolean = False
    return boolean


def newJWT(refresh_token, nickname, session):
    client = session.query(Client).filter(Client.nickname == nickname).all()
    role = session.query(Role).filter(Role.id==client[0].role_id).all()
    if not client:
        session.close()
        abort(NotFound.code)
    if not role:
        session.close()
        abort(NotFound.code)

    if security.checkRefreshToken(refresh_token, client[0].refresh_token):
        jwt = security.getToken(client[0], role[0])
    else:
        abort(Forbidden.code)

    return jwt


def refreshKeys():
    security.genKeys()
    publisher.publishKey()
    return "Keys refreshed"
