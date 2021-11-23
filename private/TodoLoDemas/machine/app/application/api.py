import requests

from . import publisher


def notifyPiecesAreDone(group):
    # r = requests.post("http://localhost:13000/notify", headers={'Content-type': 'application/json'},json={"orderID": group.order_id, "status": group.status})
    # print(r.content)
    message = {'order_id': group.order_id,
               'status': group.status}
    publisher.publish_event("produced", message)
