from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Event

from .config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=True,
                bind=engine)
        )
#Como se puede hacer esto para que no tenga que generarse el Session en esta clase, da error de dependencia circular


def create_event(routing_key, message):
    try:
        event = Event(
            routing_key=routing_key,
            message=message
        )
        session = Session()
        session.add(event)
        session.commit()
    except KeyError:
        session.rollback()
    session.close()


def read_all_events(session):
    print("GET All Events.")
    events = session.query(Event).all()
    return events


def read_event_by_id(session, event_id):
    event = session.query(Event).filter_by(id=event_id).first()
    if not event:
        session.close()
        return None
    print("GET Event {}: {}".format(event_id, event))
    return event
