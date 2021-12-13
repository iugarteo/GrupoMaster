from .device import Device


class Manager(object):
    def __init__(self):
        self.device_list = list()

    def manage_devices(self, orderId, event):
        for x in self.device_list:
            if x.orderId == orderId:
                x.on_event(event)




manager = Manager()

def getManager():
    return manager