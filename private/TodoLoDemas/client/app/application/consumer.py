import json
from types import SimpleNamespace

import pika
from . import Config, publisher, client

from .checkJWT import write_public_key_to_file
from .models import Client
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

def init_rabbitmq_event_orderDeny():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=Config.RABBIT_IP))
    channel = connection.channel()
    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)

    result = channel.queue_declare('order_deny', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='global', queue="order_deny", routing_key="order.declined")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_event_piece, auto_ack=True)

    print("Waiting for event...")
    channel.start_consuming()
    
def callback_event(ch, method, properties, body):
    print(" [x] {} {}".format(method.routing_key, body))
    message = json.loads(body)
    print(message["messagge"])
    
