import json
from datetime import datetime

import pika

from . import security


def publishKey():
    key = security.getPublicKey()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.17.2'))
    #credentials = pika.PlainCredentials('guest', 'guest')
    #parameters = pika.ConnectionParameters('192.168.17.2', 5672, '/', credentials)
    #connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='global', routing_key="client.key", body=key,
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()
    #connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.17.2'))
    #channel = connection.channel()
    #channel.queue_declare(queue='hello')
    #channel.basic_publish(exchange='global',
    #                     routing_key='client.key',
    #                        body=json.dumps(key))
    #print(" [x] Sent 'Hello World!'")
    #connection.close()

