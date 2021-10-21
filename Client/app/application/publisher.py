from . import security

def publishKey():
    security.genKeys()
    key = security.getPublicKey()
    #Publicar en la cola del rabbit el public key
    return None
