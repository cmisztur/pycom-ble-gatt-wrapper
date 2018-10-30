from network import Bluetooth

class BLEGATTSCharacteristic:
    def __init__(self, name, uuid, prop, static_read=0, dynamic_read=None, dynamic_write=None):
        self.name = name
        self.uuid = uuid
        self.static_read = static_read
        self.dynamic_read = dynamic_read
        self.dynamic_write = dynamic_write
        self.prop = prop
        self.bt_char_inst = None
        self.bt_char_cb = None

    def _characteristic_callback(self,char):
        events = char.events()
        if events & Bluetooth.CHAR_WRITE_EVENT:
            if self.dynamic_write:
                self.dynamic_write(self.name,self.uuid,char.value())
        elif events & Bluetooth.CHAR_READ_EVENT:
            if self.dynamic_read:
                return self.dynamic_read(self.name,self.uuid)
            else:
                return self.static_read

    def setInstance(self, bt_char_inst):
        self.bt_char_inst = bt_char_inst
        if self.dynamic_read or self.dynamic_write:
            self.bt_char_cb = self.bt_char_inst.callback(trigger=Bluetooth.CHAR_READ_EVENT|Bluetooth.CHAR_WRITE_EVENT, handler=self._characteristic_callback)

    def setValue(self, value):
        if self.bt_char_inst:
            self.bt_char_inst.value(value)