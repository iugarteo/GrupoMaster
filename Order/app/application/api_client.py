import json

import requests
from sqlalchemy.ext.declarative import declarative_base

from application.models import Base

Base = declarative_base()


class ApiClient:

    def create_delivery(orderid, status):
        headers = {'Content-type': 'application/json'}
        url = "http://127.0.0.1:14000/delivery"
        data = {"orderId": orderid, "status": status}
        response = requests.post(url, data =json.dumps(data), headers = headers)
        print(response)

    def request_piece_manufacturing(orderid, count):
        headers = {'Content-type': 'application/json'}
        url = "http://127.0.0.1:13000/manufacture"
        data = {"orderId": orderid, "pieces": count}
        response = requests.post(url, data = json.dumps(data), headers = headers)
        print(response)

    def request_payment(clientid):
        url = "http://127.0.0.1:12000/ask"
        headers = {'Content-type': 'application/json'}
        data = {"clientId": clientid}
        result = requests.get(url, data= json.dumps(data), headers=headers)
        print(result.text)
        return result.text

    def update_delivery_status(orderid):
        headers = {'Content-type': 'application/json'}
        url = "http://127.0.0.1:14000/deliveryDONE"
        data = {"orderId": orderid}
        response = requests.post(url, data = json.dumps(data), headers = headers)
        print(response)


