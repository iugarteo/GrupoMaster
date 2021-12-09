import json
from types import SimpleNamespace

import pika
from . import Config, publisher, order

from .checkJWT import write_public_key_to_file
from .models import Order
from .publisher import publish_event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

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

    result = channel.queue_declare('order_key', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='events', queue="order_key", routing_key="client.key")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_key, auto_ack=True)

    print("Waiting for key...")
    channel.start_consuming()


def init_rabbitmq_event():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()
    channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)

    result = channel.queue_declare('order', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='events', queue="order", routing_key="payment.accepted")
    channel.queue_bind(
        exchange='events', queue="order", routing_key="payment.declined")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_event, auto_ack=True)

    print("Waiting for event...")
    channel.start_consuming()

def init_rabbitmq_event_piece():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()
    channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)

    result = channel.queue_declare('order_piece', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='events', queue="order_piece", routing_key="machine.produced")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_event_piece, auto_ack=True)

    print("Waiting for event...")
    channel.start_consuming()


def callback_key(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    write_public_key_to_file(body)


def callback_event(ch, method, properties, body):
    from . import Session
    print(" [x] {} {}".format(method.routing_key, body))
    message = json.loads(body)
    if method.routing_key == "payment.accepted":
        session = Session()
        order = session.query(Order).get(message["order_id"])
        session.close()
        message1 = {"order_id": order.id}
        publisher.publish_event("created", message1)
        for x in range(order.number_of_pieces):
            message2 = {"order_id": order.id, "number_of_pieces": 1}
            publisher.publish_event("piece", message2)

def callback_event_piece(ch, method, properties, body):
    message = json.loads(body)
    #message2 = {"order_id": order.id, "status": "finished"}
    #publisher.publish_event("finished",message2)
    order.addPiece(message["order_id"])

