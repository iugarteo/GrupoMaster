import json

import pika


def publish_event(topic, message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.17.2'))
    channel = connection.channel()

    print(json.dumps(message))
    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)
    channel.basic_publish(
        exchange='global', routing_key="machine."+topic, body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2))
    connection.close()
