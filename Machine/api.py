import requests

def notifyPiecesAreDone(group):
    r = requests.post("http://localhost:13000/client", headers={'Content-type': 'application/json'},
                      json={"orderID": group.order_id, "status":group.status})
    print(r.content)