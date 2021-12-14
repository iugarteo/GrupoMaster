import json

import pika

from .checkJWT import write_public_key_to_file
from .logic import create_log
from . import Config


def init_rabbitmq_key():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()
    channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)

    result = channel.queue_declare('logger_key', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='events', queue="logger_key", routing_key="client.key")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_key, auto_ack=True)

    print("Waiting for key...")
    channel.start_consuming()


def init_rabbitmq_log():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()
    channel.exchange_declare(exchange='logger', exchange_type='topic', durable=True)

    result = channel.queue_declare('logger', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='logger', queue="logger", routing_key="*.*")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_event, auto_ack=True)

    print("Waiting for event...")
    channel.start_consuming()


def callback_key(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    write_public_key_to_file(body)


def callback_event(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    json_message = json.loads(body)
    create_log(json_message)
