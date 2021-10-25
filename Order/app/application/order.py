from threading import Thread, Lock, Event
import sqlalchemy
from . import Session
from .models import Order

def pedir_pago(id_o):
    session = Session()
    order = session.query(Order).get(id_o)
    numero_piezas = order.number_of_pieces
    session.close()
    precio = 100
    pago_posible = True#llamadaPayment(numero_piezas*precio)
    if(pago_posible):
        realizar_pedido(id_o)
        return "pago_posible"
    else:
        cambiar_estado("Declined")

def realizar_pedido(id_o):#Mejor en payment? Igual este metodo se va a la puta
    #maquina.create_piece(id_o)
    print("Maquina llamada para el order de id :{}".format(id_o))
    #en maquina habria que añadir uno de vuelta?
    cambiar_estado(id_o,"Finished")
    return "Maquina llamada para el order de id :{}".format(id_o)


def llamar_delivery(): #Y este igual tambien se va a la grandisima puta y en el routes llamar a las que se quieren
    printf("Piezas terminadas")
    #delivery.entregar()
    print("Entrega comenzada")

def cambiar_estado(session, order_id, status):
    if(status == "Finished" or status == "Declined"): #Comprobar que se esta introduciendo un estado existente, a created no deberia poder cambiarse de vuelta
        order = session.query(Order).get(order_id)
        #LLamar a delivery para crear uno.
        order.status = status
        print("Updated Order {} status: {}".format(order_id, order.status))
        session.commit()
        return order
    else:
        return "No existe ese estado"

def crear_order(session, content):
    new_order = None
    new_order = Order(
        description=content['description'],
        number_of_pieces=content['number_of_pieces'],
        status=Order.STATUS_CREATED
    )
    session.add(new_order)
    session.commit()
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
