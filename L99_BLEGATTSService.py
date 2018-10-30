from network import Bluetooth
from L99_BLEGATTSCharacteristic import BLEGATTSCharacteristic

class BLEGATTSService:
    def __init__(self, bt_inst, uuid):
        self.uuid = uuid
        self.bt_inst = bt_inst
        self.bt_svc_inst = None
        self.is_defined = False
        self.is_started = False
        self.characteristics = { }
 
    def start(self):
        if not self.is_defined:
            self.bt_svc_inst = self.bt_inst.service(uuid=self.uuid, isprimary=True, nbr_chars=len(self.characteristics), start=False)
            for key, char in self.characteristics.items():
                char.setInstance(self.bt_svc_inst.characteristic(uuid=char.uuid, properties=char.prop, value=char.static_read))
            self.is_defined = True

        if not self.is_started:
            self.bt_svc_inst.start()
            self.is_started = True

        return self

    def stop(self):
        if self.is_started:
            self.bt_svc_inst.stop()
            self.is_started = False

        return self

    def addReadChar(self, name, uuid, static_read=None, dynamic_read=None):
        self.characteristics[name] = BLEGATTSCharacteristic(name,uuid,Bluetooth.PROP_INDICATE|Bluetooth.PROP_BROADCAST|Bluetooth.PROP_READ,static_read=static_read,dynamic_read=dynamic_read,dynamic_write=None)
        return self#.characteristics[name]
    
    def addReadNotifyChar(self, name, uuid, static_read=None, dynamic_read=None):
        self.characteristics[name] = BLEGATTSCharacteristic(name,uuid,Bluetooth.PROP_INDICATE|Bluetooth.PROP_BROADCAST|Bluetooth.PROP_READ|Bluetooth.PROP_NOTIFY,static_read=static_read,dynamic_read=dynamic_read,dynamic_write=None)
        return self#.characteristics[name]

    def addNotifyChar(self, name, uuid, static_read=None, dynamic_read=None):
        self.characteristics[name] = BLEGATTSCharacteristic(name,uuid,Bluetooth.PROP_INDICATE|Bluetooth.PROP_BROADCAST|Bluetooth.PROP_NOTIFY,static_read=static_read,dynamic_read=dynamic_read,dynamic_write=None)
        return self#.characteristics[name]

    def addReadWriteChar(self, name, uuid, static_read=None, dynamic_read=None, dynamic_write=None):
        self.characteristics[name] = BLEGATTSCharacteristic(name,uuid,Bluetooth.PROP_INDICATE|Bluetooth.PROP_BROADCAST|Bluetooth.PROP_READ|Bluetooth.PROP_WRITE,static_read=static_read,dynamic_read=dynamic_read,dynamic_write=dynamic_write)
        return self#.characteristics[name]

    def addReadWriteNotifyChar(self, name, uuid, static_read=None, dynamic_read=None, dynamic_write=None):
        self.characteristics[name] = BLEGATTSCharacteristic(name,uuid,Bluetooth.PROP_INDICATE|Bluetooth.PROP_BROADCAST|Bluetooth.PROP_READ|Bluetooth.PROP_WRITE|Bluetooth.PROP_NOTIFY,static_read=static_read,dynamic_read=dynamic_read,dynamic_write=dynamic_write)
        return self#.characteristics[name]