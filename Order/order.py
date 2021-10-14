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
        #Discutir si la comparación iria mejor en payment porque es la que tiene la cartera, de esta manera Order solo manda una message con el coste
        #Y en caso de valido llame a realizar_pedio o al microservicio de maquina
        coste = session.query(Piece).get(coste)
        if(coste > 2):
            print("Nope, no hay dinero")
            cambiar_estado("Declined")
        if(coste2 <= 2):
            print("Pedido mandado a produccion")
            realizar_pedido(1)
        #if(posible):
        #    reaizar_pedido()
        #else:
        #    cambiar_estado("Declined")

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
        if(status == "Finished" or status == "Declined"):
            session = Session()
            order = session.query(Order).get(order_id)
            order.status = Order.status
            print("Updated Order {} status: {}".format(order_is, order.status))
            session.commit()
            session.rollback()
            session.close()
            return order
        else:
            return "No existe ese estado"
##Parece un select --> manufacturing_piece = self.thread_session.query(Piece).filter_by(status=Piece.STATUS_MANUFACTURING).first()