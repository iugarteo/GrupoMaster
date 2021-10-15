import bcrypt
import jwt


def hashPassword(passw):
    salt = bcrypt.gensalt()
    passEnc = bcrypt.hashpw(passw.encode('utf-8'), salt)
    return passEnc.decode()

def checkPass(password, client):
    if bcrypt.checkpw(password.encode('utf-8'), client.password.encode('utf-8')):
        auth = True
    else:
        auth = False
    return auth

def getToken(nickname, password):
    encoded = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
    #print(generateKeys())
    #print(encoded)
    #print(jwt.decode(encoded, "secret", algorithms=["HS256"]))
    return encoded