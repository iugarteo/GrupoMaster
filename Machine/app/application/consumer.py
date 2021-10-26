import json
from types import SimpleNamespace

import pika
from . import Config


from Machine.app.application.publisher import publish_event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from .checkJWT import set_public_key
from .machine import Machine
from .models import PieceGroup, Piece

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

    result = channel.queue_declare('machine_key', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='global', queue="machine_key", routing_key="client.key")

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback_key, auto_ack=True)

    print("Waiting for key...")
    channel.start_consuming()


def init_rabbitmq_event():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.17.2'))
    channel = connection.channel()
    channel.exchange_declare(exchange='global', exchange_type='topic', durable=True)

    result = channel.queue_declare('machine', durable=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange='global', queue="machine", routing_key="order.md")

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
    my_machine = Machine()
    session = Session()
    try:
        new_PieceGroup = PieceGroup(
            order_id=message['order_id'],
            number_of_pieces=message['number_of_pieces'],
            status="Created"
        )
        session.add(new_PieceGroup)
        for i in range(new_PieceGroup.number_of_pieces):
            piece = Piece()
            piece.group = new_PieceGroup
            session.add(piece)
        session.commit()
        my_machine.add_pieces_to_queue(new_PieceGroup.pieces)
        session.commit()
    except KeyError:
        session.rollback()
        session.close()

