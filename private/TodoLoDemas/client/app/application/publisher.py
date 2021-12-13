import json

import pika

from . import security
from . import Config


def publishKey():
    key = security.getPublicKey()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()

    channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='events', routing_key="client.key", body=key,
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()


def publish_log(timestamp, service_name, severity, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()

    log = {
        "timestamp": timestamp,
        "service": service_name,
        "severity": severity,
        "message": message}
    print(log)

    channel.exchange_declare(exchange='logger', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='logger', routing_key=service_name + "." + severity, body=json.dumps(log),
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()

