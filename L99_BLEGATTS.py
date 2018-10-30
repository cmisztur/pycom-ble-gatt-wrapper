from network import Bluetooth
from L99_BLEGATTSService import BLEGATTSService

class BLEGATTS:
    def __init__(self):
        self.bt_inst = None
        self.advert_name = None
        self.connect_callback = None
        self.is_connected = False
        self.services = { }

    def _connection_handler(self, bt):
        events = bt.events()
        if events & Bluetooth.CLIENT_CONNECTED:
            self.is_connected = True
            if self.connect_callback: 
                self.connect_callback(self.is_connected)
        elif events & Bluetooth.CLIENT_DISCONNECTED:
            self.is_connected = False
            if self.connect_callback: 
                self.connect_callback(self.is_connected)

    def init(self, advert_name, connect_callback = None):
        self.bt_inst = Bluetooth(id=0,antenna=Bluetooth.INT_ANT)
        self.advert_name = advert_name
        self.connect_callback = connect_callback
        self.bt_inst.set_advertisement(name=self.advert_name, manufacturer_data=None, service_data=None, service_uuid=None)
        self.bt_inst.callback(trigger=Bluetooth.CLIENT_CONNECTED|Bluetooth.CLIENT_DISCONNECTED, handler=self._connection_handler)

    def advertise(self, toggle=True):
        self.bt_inst.advertise(toggle)

    def disconnect(self):
        if self.is_connected:
            self.bt_inst.disconnect_client()

    def deinit(self):
        #TODO: stop services
        self.disconnect()
        self.bt_inst.deinit()

    def addService(self, service_name, uuid):
        self.services[service_name] = BLEGATTSService(self.bt_inst, uuid)
        return self.services[service_name]

    def getService(self, service_name):
        return service_name in self.services and self.services[service_name] or None

    def setCharValue(self, svc_name, char_name, value):
        if self.is_connected and svc_name in self.services and char_name in self.services[svc_name].characteristics:
            #print ('%s:%s=%s' % (svc_name,char_name,str(value)))
            self.services[svc_name].characteristics[char_name].setValue(value)