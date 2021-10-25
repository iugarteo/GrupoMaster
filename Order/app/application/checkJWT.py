import jwt
from werkzeug.exceptions import Forbidden, abort

from . import consumer

public_key = ""

def readToken(encoded, public_key):
    print(public_key)

    try:
        decoded = jwt.decode(encoded, public_key, algorithms=["RS256"])
    except jwt.ExpiredSignatureError:
        print("ERROR: Signature expired")
        return abort(Forbidden.code)
    except jwt.InvalidSignatureError:
        print("ERROR: Invalid Signature")
        return abort(Forbidden.code)
    # Signature has expired
    return decoded

def checkPermissions(permision, token):
    print(public_key)
    decoded = readToken(token, public_key)
    if decoded == None:
        return False
    else:
        permisions = decoded["Permisions"].split(",")
    if permision in permisions:
        boolean = True
    else:
        boolean = False
    return boolean

def setKey(key):
    global public_key
    public_key = key
