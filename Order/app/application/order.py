from threading import Thread, Lock, Event
import sqlalchemy
import json
from . import publisher
from . import Session
from .models import Order

def pedir_pago(order): #Cambios en este metodo
    
    precio = order.price_total
    message_pieces = {"price": precio,"client_id": order.client_id,"order_id": order.id} #No se cuales serian los metodos
    publisher.publish_event("create", message_pieces) #No se cual seria la cola

def cambiar_estado(session, order_id, status):
    if(status == "Finished" or status == "Declined" or status == "Pending on payment" or status == "Acepted"): #Comprobar que se esta introduciendo un estado existente, a created no deberia poder cambiarse de vuelta
        order = session.query(Order).get(order_id)
        #LLamar a delivery para crear uno.
        order.status = status
        print("Updated Order {} status: {}".format(order_id, order.status))
        session.commit()
        return order
    else:
        return "No existe ese estado"

def crear_order(session, content): #Cambios en este metodo
    new_order = None
    new_order = Order(
        client_id=content['client_id'],
        number_of_pieces=content['number_of_pieces'],
        price_total=content['number_of_pieces'] * 30,
        description=content['description'],
        status=Order.STATUS_CREATED
    )
    session.add(new_order)
    session.commit()
    pedir_pago(new_order)

    session.close()
    return new_order

def ver_order_id(session, id):
    new_order =  session.query(Order).get(id)
    return new_order

def ver_orders(session):
    orders = session.query(Order).all()
    return orders

def delete_order(session):
    session.delete()
    session.commit()
