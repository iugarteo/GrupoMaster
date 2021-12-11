import json

import pika
from . import Config


def publish_event(topic, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()

    print(json.dumps(message))
    channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='events', routing_key="delivery."+topic, body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()
