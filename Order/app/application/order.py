from threading import Thread, Lock, Event
import sqlalchemy
import json
from . import publisher
from . import Session
from .models import Order

def pedir_pago(id_o): #Cambios en este metodo
    session = Session()
    order = session.query(Order).get(id_o)
    numero_piezas = order.number_of_pieces
    session.close()
    precio = order.price_total
    message_pieces = {"precio": precio,"client_id": new_order.client_id} #No se cuales serian los metodos
    publish_event("md", json.dump(message_pieces)) #No se cual seria la cola
    pago_posible = True #llamada al consumer para obtener lo que mande payment
    if(pago_posible):
        return True
    else:
        return False

""" Todo esto deberia ser borrable
def realizar_pedido(id_o):#Esto hay que mandarlo a la putisima, no sirve de nada
    #maquina.create_piece(id_o)
    print("Maquina llamada para el order de id :{}".format(id_o))
    #en maquina habria que añadir uno de vuelta?
    cambiar_estado(id_o,"Finished")
    return "Maquina llamada para el order de id :{}".format(id_o) 


def llamar_delivery(): #Y este tambien a la putisima mas puta
    printf("Piezas terminadas")
    #delivery.entregar()
    print("Entrega comenzada") """

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
    if pedir_pago(new_order.id): #Primero iria el comprobar si es posible antes de llamar a delivery y machine
        session.close()
        message_pieces = {"number_of_pieces": content['number_of_pieces'],"order_id": new_order.id}
        publish_event("md", json.dump(message_pieces))
    else:
        status=Order.STATUS_DECLINED
        session.commit()
        session.close()
    return new_order

def ver_order_id(session, id):
    new_order =  session.query(Order).get(id)
    return new_order

def ver_orders(session):
    orders = session.query(Order).all()
    return orders

def delete_order(session):
    session.delete(order)
    session.commit()
