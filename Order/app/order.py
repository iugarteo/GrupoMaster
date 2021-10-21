from threading import Thread, Lock, Event
import sqlalchemy
from . import Session

class Order(Thread):
    STATUS_CREATED = "Created"
    STATUS_FINISHED = "Finished"
    STATUS_DECLINED = "Declined"
    thread_session = None

    def __init__(self, num_p):
        self.status = Order.STATUS_CREATED
        self.num_pieces = num_p
        self.instance = self

    def pedir_pago(self, id_p):
        coste = session.query(Piece).filter_by(ref=id_p).get(coste)
        pago_posible = llamadaPayment(coste)
        if(pago_posible):
            realizar_pedido()
        else:
            cambiar_estado("Declined")

    def realizar_pedido(self, id_o):#Mejor en payment? Igual este metodo se va a la puta
        #maquina.create_piece(id_o)
        print("Maquina llamada para el order de id :{}".format(id_o))
        #en maquina habria que añadir uno de vuelta?
        cambiar_estado("Finished")


    def llamar_delivery(self): #Y este igual tambien se va a la grandisima puta y en el routes llamar a las que se quieren
        printf("Piezas terminadas")
        #delivery.entregar()
        print("Entrega comenzada")

    def cambiar_estado(self, order_id, status):
        if(status == "Finished" or status == "Declined"): #Comprobar que se esta introduciendo un estado existente, a created no deberia poder cambiarse de vuelta
            session = Session()
            order = session.query(Order).get(order_id)
            #LLamar a delivery para crear uno.
            order.status = Order.status
            print("Updated Order {} status: {}".format(order_is, order.status))
            session.commit()
            session.rollback()
            session.close()
            return order
        else:
            return "No existe ese estado"