import json

import pika
from flask import request

from . import Config
from .BLConsul import SERVICE_ID, SERVICE_NAME


def publish_response(topic, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()

    print(json.dumps(message))
    channel.exchange_declare(exchange='responses', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='responses', routing_key="payment."+topic, body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()


def publish_log(timestamp, severity, message, filename=None, function=None):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()

    log = {
        "timestamp": timestamp,
        "url": request.base_url,
        "request_body": request.data.decode("utf-8"),
        "service": SERVICE_NAME,
        "service_id": SERVICE_ID,
        "severity": severity,
        "filename": filename,
        "function": function,
        "message": str(message)
    }
    print(log)

    channel.exchange_declare(exchange='logger', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='logger', routing_key=SERVICE_NAME + "." + severity, body=json.dumps(log).encode('utf8'),
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()
