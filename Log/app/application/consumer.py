import json
from datetime import datetime
from types import SimpleNamespace

import pika

from .logic import create_event


def init_rabbitmq():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.17.2'))
    channel = connection.channel()
    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)

    result = channel.queue_declare('log', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='global', queue="log", routing_key="*.*")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("Waiting for event...")
    channel.start_consuming()


def write_log_to_file(log):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_message = str(log, 'UTF-8')
    obj = json.loads(log_message, object_hook=lambda d: SimpleNamespace(**d))

    try:
        file = open("./logs/log_" + obj.severity + "_" + date + ".txt", "a")
        file.write(timestamp + ": " + log_message + '\n')
        file.close()
    except FileNotFoundError:
        print("Error")


def callback(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    if method.routing_key == 'client.key':
        body = 'Public key created'
    create_event(method.routing_key, body)
