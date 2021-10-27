import json
import threading
from types import SimpleNamespace

import pika
from . import Config

from .checkJWT import set_public_key
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from .delivery import update_delivery_by_order, create_delivery
from .models import Delivery

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=True,
                bind=engine)
        )

public_key = None


def init_rabbitmq_key():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.17.2'))
       
    channel = connection.channel()
    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)

    result = channel.queue_declare('delivery_key', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='global', queue="delivery_key", routing_key="client.key")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_key, auto_ack=True)

    print("Waiting for key...")
    channel.start_consuming()


def init_rabbitmq_event(queue, routing_key, callback):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.17.2'))
        #pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)

    result = channel.queue_declare(queue, durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='global', queue=queue, routing_key=routing_key)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("Waiting for event...")
    channel.start_consuming()


def callback_key(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    set_public_key(body)


def callback_order_event(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    message = json.loads(body, object_hook=lambda d: SimpleNamespace(**d))
    session = Session()
    delivery = create_delivery(session, message.order_id)
    if not delivery:
        print("Error during delivery registration with {} order_id".format(message.order_id))
    session.close()


def callback_machine_event(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    message = json.loads(body, object_hook=lambda d: SimpleNamespace(**d))
    session = Session()
    delivery = update_delivery_by_order(session, message.order_id, Delivery.STATUS_SENT)
    if delivery:
        # sleep for 10 seconds
        update_delivery_by_order(session, message.order_id, Delivery.STATUS_RECEIVED)
    else:
        print("Error while updating delivery with {} order_id".format(message.order_id))
    session.close()
