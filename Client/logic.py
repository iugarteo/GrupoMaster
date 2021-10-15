
from . import Session
from flask import request, jsonify, abort
from .models import Client
from werkzeug.exceptions import NotFound, InternalServerError, BadRequest, UnsupportedMediaType
from . import security
#from Crypto.PublicKey import RSA

#def generateKeys():
#    key = RSA.generate(2048)
 #   f = open('mykey.pem','wb')
  #  f.write(key.export_key('PEM'))
   # f.close()
    #f = open('mykey.pem','r')
    #key = RSA.import_key(f.read())
    #return key

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

def authentication(nickname, password):
    session = Session()
    client = session.query(Client).filter(Client.nickname==nickname).all()
    if not client:
        session.close()
        abort(NotFound.code)
    auth = security.checkPass(password, client[0])
    session.close()
    if (auth == True):
        print("Authentication correct!")
        response = security.getToken(nickname, password)
    else:
        print("Authentication incorrect! ERROR!!!!!!")
        abort(BadRequest.code)
    return response

