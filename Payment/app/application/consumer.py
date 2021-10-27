import json
from types import SimpleNamespace

import pika
from . import Config

from .checkJWT import set_public_key
from .payment_service import payment_validation
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
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)

    result = channel.queue_declare('payment_key', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='global', queue="payment_key", routing_key="client.key")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_key, auto_ack=True)

    print("Waiting for key...")
    channel.start_consuming()


def init_rabbitmq_event():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.17.2'))
    channel = connection.channel()
    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)

    result = channel.queue_declare('payment', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='global', queue="payment", routing_key="order.pago")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_event, auto_ack=True)

    print("Waiting for event...")
    channel.start_consuming()


def callback_key(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    set_public_key(body)


def callback_event(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    message = json.loads(body, object_hook=lambda d: SimpleNamespace(**d))
    session = Session()
    valid = payment_validation(session, message["client_id"], message["price"])
    print(valid)
    session.close()
    if valid:
        status = 'accepted'
    else:
        status = 'declined'
    result = {'client_id': message.client_id,
              'payment_id': message.payment_id,
              'status': status}
    publish_event("status", result)
