from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Log

from .config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=True,
                bind=engine)
        )
#Como se puede hacer esto para que no tenga que generarse el Session en esta clase, da error de dependencia circular


def create_log(json_message):
    try:
        log = Log(
            timestamp=json_message["timestamp"],
            url=json_message["url"],
            request_body=json_message["request_body"],
            service=json_message["service"],
            service_id=json_message["service_id"],
            severity=json_message["severity"],
            filename=json_message["filename"],
            function=json_message["function"],
            message=json_message["message"]
        )
        session = Session()
        session.add(log)
        session.commit()
    except KeyError:
        session.rollback()
    session.close()


def read_all_logs(session):
    print("GET All Logs.")
    events = session.query(Log).all()
    return events


def read_log_by_id(session, event_id):
    event = session.query(Log).filter_by(id=event_id).first()
    if not event:
        session.close()
        return None
    print("GET Event {}: {}".format(event_id, event))
    return event


# def read_logs_by_severity():

# def read_logs_by_service():
