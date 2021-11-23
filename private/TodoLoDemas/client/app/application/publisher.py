import json
from datetime import datetime

import pika

from . import security
from . import Config

def publishKey():
    key = security.getPublicKey()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()

    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='global', routing_key="client.key", body=key,
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()
