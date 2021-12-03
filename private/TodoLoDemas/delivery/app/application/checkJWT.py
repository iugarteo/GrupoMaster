import jwt
from werkzeug.exceptions import Forbidden, abort
import threading

mutex = threading.Lock()
public_key = ''


def readToken(encoded, public_key):

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

    decoded = readToken(token, public_key)
    if decoded == None:
        return False
    else:
        #zip_code = decoded["Zip"]
        permisions = decoded["Permisions"].split(",")
    if permision in permisions:
        boolean = True
    else:
        boolean = False
    return boolean

def checkZIP(token):

    decoded = readToken(token, public_key)
    #zip_code = decoded["Zip"]
    #if (zip_code != 1 or zip_code != 20 or zip_code != 48)
        #message_pieces = {"price": precio,"client_id": order.client_id,"order_id": order.id} 
        #publisher.publish_event("declined", message_pieces)

def load_public_key_from_file():
    try:
        mutex.acquire()
        file = open(r"./public_key.pem", "rb")
        global public_key
        public_key = file.read().decode("utf-8")
        file.close()
    except Exception:
        print("Error al leer la clave pública del fichero")
    finally:
        mutex.release()


def write_public_key_to_file(key):
    try:
        mutex.acquire()
        global public_key
        public_key = key
        file = open(r"./public_key.pem", "w")
        file.write(key.decode())
        file.close()
    except Exception:
        print("Error al escribir la clave pública en el fichero")
    finally:
        mutex.release()
