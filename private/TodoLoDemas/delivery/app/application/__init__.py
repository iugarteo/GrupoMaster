import threading

from flask import Flask
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from .BLConsul import BLConsul
from .config import Config
from .consumer import init_rabbitmq_key, init_rabbitmq_event, callback_order_event, callback_finish_event, callback_check_event
from .checkJWT import load_public_key_from_file

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=True,
                bind=engine)
        )


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():
        from . import routes
        from . import models

        bl_consul = BLConsul.get_instance()
        bl_consul.init_and_register(app)

        load_public_key_from_file()

        key_consumer = threading.Thread(target=init_rabbitmq_key)
        key_consumer.start()

        event_consumer1 = threading.Thread(target=init_rabbitmq_event,
                                           args=('delivery_order', 'order.created', callback_order_event))
        event_consumer1.start()

        event_consumer2 = threading.Thread(target=init_rabbitmq_event,
                                           args=('delivery_finish', 'order.finished', callback_finish_event))
        event_consumer2.start()

        event_consumer3 = threading.Thread(target=init_rabbitmq_event,
                                           args=('delivery_check', 'order.checkAddress', callback_check_event))
        event_consumer3.start()

        models.Base.metadata.create_all(engine)
        return app
