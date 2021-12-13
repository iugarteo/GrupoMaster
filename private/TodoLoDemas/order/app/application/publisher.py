import json
from datetime import datetime

import pika
from flask import jsonify

from . import Config


def publish_event(topic, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()

    print(json.dumps(message))
    channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='events', routing_key="order."+topic, body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()


def publish_log(service, level, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()

    datetime_object = datetime.now()
    timestamp = datetime_object.strftime("%d-%b-%Y %H:%M:%S:%f")
    log = jsonify(timestamp=timestamp, service=service, level=level, message=message)

    print(json.dumps(message))
    channel.exchange_declare(exchange='logger', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='logger', routing_key=service + "." + level, body=log,
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()
