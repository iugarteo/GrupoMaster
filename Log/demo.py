import json
from types import SimpleNamespace

import pika
from datetime import datetime

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='payment', exchange_type='topic')

result = channel.queue_declare('log', durable=True)
queue_name = result.method.queue


def write_log_to_file(log):
    now = datetime.now()
    date = now.strftime("%m-%d-%Y")
    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
    log_message = str(log, 'UTF-8')
    obj = json.loads(log_message, object_hook=lambda d: SimpleNamespace(**d))

    file = open("./logs/log_"+obj.severity+"_"+date+".txt", "a")
    file.write(timestamp+": "+log_message + '\n')
    file.close()


def callback(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    write_log_to_file(body)


channel.queue_bind(
        exchange='payment', queue="log", routing_key="*.*")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Waiting for event...")
channel.start_consuming()
