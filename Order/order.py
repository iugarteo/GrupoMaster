from threading import Thread, Lock, Event
import sqlalchemy
from . import Session


#los imports

class Order(Thread):
    STATUS_CREATED = "Created"
    STATUS_FINISHED = "Finished"
    STATUS_DECLINED = "Declined"
    thread_session = None

    def __init__(self, num_p):
        self.status = Order.STATUS_CREATED
        self.num_pieces = num_p
        self.instance = self

    def pedir_pago(self, id_c, id_p):
        #Discutir si la comparación iria mejor en payment porque es la que tiene la cartera, de esta manera Order solo manda una message con el coste
        #Y en caso de valido llame a realizar_pedio o al microservicio de maquina
        dinero = self.thread_session.query(Cartera).filter_By(id_cartera = id_c).first()
        coste = self.thread_session.query(Pieza).filter_By(id_pieza = id_p).first()
        if(monedero < coste * self.num_pieces):
            self.actualizar_estado("Declined")
            return "No hay saldo suficiente"
        else:
            Payment.reducirSaldo()
            self.realizar_pedido()

    def realizar_pedido(self, id_o):#Mejor en payment?
        maquina.create_piece(id_o)
        #en maquina habria que añadir uno de vuelta?


    def llamar_delivery(self):
        printf("Piezas terminadas")
        delivery.entregar()


##Parece un select --> manufacturing_piece = self.thread_session.query(Piece).filter_by(status=Piece.STATUS_MANUFACTURING).first()