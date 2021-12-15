import json

import pika
from . import Config

from .checkJWT import write_public_key_to_file
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from .delivery import update_delivery_by_order, create_delivery
from .models import Delivery
from .publisher import publish_response

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
        pika.ConnectionParameters(host=Config.RABBIT_IP))
       
    channel = connection.channel()
    channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)

    result = channel.queue_declare('delivery_key', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='events', queue="delivery_key", routing_key="client.key")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_key, auto_ack=True)

    print("Waiting for key...")
    channel.start_consuming()


def init_rabbitmq_event(queue, routing_key, callback, exchange):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='topic', durable=True)

    result = channel.queue_declare(queue, durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange=exchange, queue=queue, routing_key=routing_key)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("Waiting for event...")
    channel.start_consuming()


def callback_key(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    write_public_key_to_file(body)


def callback_order_event(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    message = json.loads(body)
    session = Session()
    delivery = create_delivery(session, message["order_id"])
    if not delivery:
        print("Error during delivery registration with {} order_id".format(message.order_id))
    session.close()


def callback_finish_event(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    message = json.loads(body)
    session = Session()
    delivery = update_delivery_by_order(session, message["order_id"], Delivery.STATUS_SENT)
    if delivery:
        # sleep for 10 seconds
        update_delivery_by_order(session, message["order_id"], Delivery.STATUS_RECEIVED)
    else:
        print("Error while updating delivery with {} order_id".format(message.order_id))
    session.close()

def callback_check_event(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    message = json.loads(body)
    topic = message["topic"]
    if (message["zipCode"] == "01") or (message["zipCode"] == "20") or (message["zipCode"] == "48"):
        message = {"orderId":message["orderId"],"check":"Accepted"}
        publish_response(topic, message)
    else:
        message = {"orderId": message["orderId"], "check": "Declined"}
        publish_response(topic, message)
