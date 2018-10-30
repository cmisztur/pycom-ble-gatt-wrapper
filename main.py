import gc
import machine
import utime
import ubinascii
import uos
from machine import Timer

from L99_BLEGATTS import BLEGATTS

hardware_serial = ubinascii.hexlify(machine.unique_id()).decode()
l99_serial = 'L99-%s' % hardware_serial

def ble_connection_callback(is_connected):
    if is_connected: 
        print("BLE connected")
    else:
        print("BLE disconnected")

ble = BLEGATTS()
ble.init(advert_name=l99_serial, connect_callback=ble_connection_callback)

ble.addService(service_name='device_info',uuid=6154) \
    .addReadChar (name='l99_serial', uuid=0, static_read=l99_serial) \
    .addReadChar (name='hardware_serial', uuid=1, static_read=hardware_serial) \
    .addReadChar (name='sysname', uuid=2, dynamic_read=lambda cn,id: uos.uname()[0]) \
    .addReadChar (name='nodename', uuid=3, dynamic_read=lambda cn,id: uos.uname()[1]) \
    .addReadChar (name='release', uuid=4, dynamic_read=lambda cn,id: uos.uname()[2]) \
    .addReadChar (name='version_number', uuid=5, dynamic_read=lambda cn,id: uos.uname()[3].split(' on ')[0]) \
    .addReadChar (name='version_date', uuid=6, dynamic_read=lambda cn,id: uos.uname()[3].split(' on ')[1]) \
    .addReadChar (name='machine', uuid=7, dynamic_read=lambda cn,id: uos.uname()[4]) \
    .addReadChar (name='lora_version', uuid=8, dynamic_read=lambda cn,id: uos.uname()[5]) \
    .start()

ble.addService(service_name='char_tests',uuid=0) \
    .addNotifyChar (name='note1', uuid=0, static_read=0) \
    .addReadNotifyChar (name='note2', uuid=1, static_read=0) \
    .addReadChar (name='self', uuid=2, dynamic_read=lambda cn,id: cn+str(id)) \
    .addReadWriteChar (name='r+w', uuid=3,
                        dynamic_read=lambda cn,id: char_rw_test_read(cn,id),
                        dynamic_write=lambda cn,id,val: char_rw_test_write(cn,id,val)) \
    .addReadWriteNotifyChar (name='r+w+n', uuid=4,
                            dynamic_read=lambda cn,id: char_rwn_test_read(cn,id),
                            dynamic_write=lambda cn,id,val: char_rwn_test_write(cn,id,val)) \
    .start()

ble.advertise()

rw_var = 1337

def char_rw_test_read(char_name,char_uuid):
    global rw_var
    return rw_var

def char_rw_test_write(char_name,char_uuid,char_value):
    global rw_var
    rw_var = char_value

def char_rwn_test_read(char_name,char_uuid):
    global rw_var
    return rw_var

def char_rwn_test_write(char_name,char_uuid,char_value):
    global rw_var
    rw_var = char_value
    global ble
    ble.setCharValue('char_tests','r+w+n',rw_var) # ain't gonna notify itself

def char_timer(t):
    global counter
    counter = counter + 1
    ble.setCharValue('char_tests','note1',counter)
    ble.setCharValue('char_tests','note2',counter) # i can only get one or the other to notify, but not both

counter = 1
timer = Timer.Alarm(handler=char_timer, ms=2000, periodic=True)

'''
try:
    while True:
        machine.idle()
except:
    pass
'''