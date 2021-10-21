from .models import Client


def view_client_by_id(session, client_id):
    client = session.query(Client).get(client_id)
    if not client:
        session.close()
        return None
    print("GET Client {}: {}".format(client_id, client))
    return client

def view_all_clients(session):
    print("GET All Clients")
    clients = session.query(Client).all()
    return clients


def create_client(session, name, surname):
    session = Session()
    new_client = None
    try:
        new_client = Client(
            name=name,
            surname=surname
        )
        session.add(new_client)

        session.commit()
        session.commit()
    except KeyError:
        session.rollback()
        session.close()
        abort(BadRequest.code)
    return new_client
