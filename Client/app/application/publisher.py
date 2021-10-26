import json
from datetime import datetime

import pika

from . import security


def publishKey():
    key = security.getPublicKey()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    message = {'client_id': 1,
                'payment_id': 1,
                'price': 10}

    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='global', routing_key="client.key", body=key,
        #exchange='global', routing_key="order.create", body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()
