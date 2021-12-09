import json
from types import SimpleNamespace

import pika
from . import Config

from .checkJWT import write_public_key_to_file
from .payment_service import payment_validation, view_account, create_payment
from . import publisher
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=True,
                bind=engine)
        )


def init_rabbitmq_key():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()
    channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)

    result = channel.queue_declare('payment_key', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='events', queue="payment_key", routing_key="client.key")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_key, auto_ack=True)

    print("Waiting for key...")
    channel.start_consuming()


def init_rabbitmq_event():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()
    channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)

    result = channel.queue_declare('payment', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='events', queue="payment", routing_key="order.create")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_event, auto_ack=True)

    print("Waiting for event...")
    channel.start_consuming()


def callback_key(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    write_public_key_to_file(body)


def callback_event(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    message = json.loads(body)
    session = Session()
    valid = payment_validation(session, message["client_id"], message["price"])
    print(valid)
    if valid:
        status = 'accepted'
        account = view_account(session, message["client_id"])
        create_payment(session, account, message["client_id"], message["price"])
    else:
        status = 'declined'
    session.close()
    result = {'client_id': message["client_id"],
              'payment_id': message["price"],
              'order_id': message["order_id"],
              'status': status}
    publisher.publish_event(status, result)
