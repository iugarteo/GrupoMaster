import threading
from flask import Flask
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

from .BLConsul import BLConsul
from .checkJWT import load_public_key_from_file
from .config import Config
from .consumer import init_rabbitmq_event, init_rabbitmq_key

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
        models.Base.metadata.create_all(engine)

        bl_consul = BLConsul.get_instance()
        bl_consul.init_and_register(app)

        load_public_key_from_file()

        key_consumer = threading.Thread(target=init_rabbitmq_key)
        key_consumer.start()

        event_consumer = threading.Thread(target=init_rabbitmq_event)
        event_consumer.start()

        return app
