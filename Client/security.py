import bcrypt
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

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

def getToken(nickname):
    private_key = getPrivateKey()
    encoded = jwt.encode({"Hire ama": "pelele"}, private_key, algorithm="RS256")
    return encoded

def readToken(encoded, public_key):

    try:
        decoded = jwt.decode(encoded, public_key, algorithms=["RS256"])
    except jwt.ExpiredSignatureError:
        print("ERROR: Signature expired")
    except jwt.InvalidSignatureError:
        print("ERROR: Invalid Signature")
    # Signature has expired
    return decoded

def genKeys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    private_key_pass = b"password_encode_key"

    encrypted_pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(private_key_pass)
    )

    pem_public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    private_key_file = open("private_key.pem", "w")
    private_key_file.write(encrypted_pem_private_key.decode())
    private_key_file.close()

    public_key_file = open("public_key.pem", "w")
    public_key_file.write(pem_public_key.decode())
    public_key_file.close()
    token=getToken("Mendilu")
    print(readToken(token,getPublicKey()))

    return pem_public_key, private_key

def getPublicKey():
    public_key_file = open("public_key.pem", "rb")
    public_key = public_key_file.read().decode("utf-8")
    public_key_file.close()
    print(public_key)
    return public_key

def getPrivateKey():
    private_key_file = open("private_key.pem", "rb")
    private_key = serialization.load_pem_private_key(private_key_file.read(), b"password_encode_key")
    private_key_file.close()
    return private_key