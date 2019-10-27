# -*- coding: utf-8 -*-
# License: GNU General Public License, Version 3

import struct, time, random
from bluetooth import BLE, UUID, FLAG_NOTIFY, FLAG_READ, FLAG_WRITE
from micropython import const
from ble_advertising import advertising_payload
#from terkin import logging

_IRQ_CENTRAL_CONNECT                 = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT              = const(1 << 1)

# org.bluetooth.service.battery_service - BS
_BS_INT = 0x180F
_BS_UUID = UUID(_BS_INT)
# org.bluetooth.characteristic.battery_level
_BS_CHAR = (UUID(0x2A19), FLAG_READ | FLAG_NOTIFY,)
_BS_SERVICE = (_BS_UUID, (_BS_CHAR,), )

# org.bluetooth.service.weight_scale - WS
_WS_INT = 0x181D
_WS_UUID = UUID(_WS_INT)
# org.bluetooth.characteristic.weight_measurement
_WS_CHAR = (UUID(0x2A9D), FLAG_READ | FLAG_NOTIFY,)
_WS_SERVICE = (_WS_UUID, (_WS_CHAR,), )

# org.bluetooth.service.environmental_sensing - ES
_ES_INT = 0x181A
_ES_UUID = UUID(_ES_INT)
# org.bluetooth.characteristic.humidity
_ES_CHAR_HUM = (UUID(0x2A6F), FLAG_READ | FLAG_NOTIFY,)
# org.bluetooth.characteristic.temperature
_ES_CHAR_TEMP = (UUID(0x2A6E), FLAG_READ | FLAG_NOTIFY,)
_ES_SERVICE = (_ES_UUID, (_ES_CHAR_HUM, _ES_CHAR_TEMP,), )

# org.bluetooth.service.generic_access - GA
_GA_INT = 0x1800
_GA_UUID = UUID(_GA_INT)
# org.bluetooth.characteristic.gap.device_name
_GA_CHAR_NAME = (UUID(0x2A00), FLAG_READ | FLAG_NOTIFY,)
# org.bluetooth.characteristic.gap.appearance
_GA_CHAR_APP =  (UUID(0x2A01), FLAG_READ | FLAG_NOTIFY,)
_GA_SERVICE = (_GA_UUID, (_GA_CHAR_NAME, _GA_CHAR_APP,), )

# org.bluetooth.service.current_time - CT
_CT_INT = 0x1805
_CT_UUID = UUID(0x1805)
# org.bluetooth.characteristic.weight_measurement
_CT_CHAR = (UUID(0x2A00), FLAG_READ | FLAG_NOTIFY,)
_CT_SERVICE = (_CT_UUID, (_CT_CHAR,), )

# Hiveeyes (HE) service for temperature sensors inside the brood box (TB)
_HE_TB_UUID = UUID('04500100-39fd-49ec-b565-b5d6dc31b6ae')
# characteristics: 10 temperature sensors
_HE_TB_CHAR_T01 = (UUID('04500101-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
_HE_TB_CHAR_T02 = (UUID('04500102-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
_HE_TB_CHAR_T03 = (UUID('04500103-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
_HE_TB_CHAR_T04 = (UUID('04500104-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
_HE_TB_CHAR_T05 = (UUID('04500105-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
_HE_TB_CHAR_T06 = (UUID('04500106-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
_HE_TB_CHAR_T07 = (UUID('04500107-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
_HE_TB_CHAR_T08 = (UUID('04500108-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
_HE_TB_CHAR_T09 = (UUID('04500109-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
_HE_TB_CHAR_T10 = (UUID('04500110-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
# servive list
_HE_TB_SERVICE = (_HE_TB_UUID, (_HE_TB_CHAR_T01, _HE_TB_CHAR_T02, _HE_TB_CHAR_T03, _HE_TB_CHAR_T04, _HE_TB_CHAR_T05, _HE_TB_CHAR_T06, _HE_TB_CHAR_T07, _HE_TB_CHAR_T08, _HE_TB_CHAR_T09, _HE_TB_CHAR_T10, ), )

# services you can get data from
_SERVICES = (_BS_SERVICE, _WS_SERVICE,_ES_SERVICE,_HE_TB_SERVICE)
# advertised services
_ADV_SERVICES = [_BS_UUID,_WS_UUID,_ES_UUID,]
# set appearance - sets the icon
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_WEIGHT_SCALE = const(3200)

#log = logging.getLogger(__name__)

class BluetoothApiESP32:
    """
    
    """

    def __init__(self, ble, name='HEN'):    # HiveEyesNode
        """
        Start BLE & Advertising
        """
        #self._reading = reading  # last_reading from datalogger.storage
        self._ble = ble
        print('Starting BLE')
        self.start()    
        self._ble.irq(handler=self._irq)
        ((self._BS_handle,),(self._WS_handle,),(self._ES_HUM_handle, self._ES_TEMP_handle,), \
            (self._TB_T01_handle, self._TB_T02_handle, self._TB_T03_handle, self._TB_T04_handle, \
             self._TB_T05_handle, self._TB_T06_handle, self._TB_T07_handle, self._TB_T08_handle, \
             self._TB_T09_handle, self._TB_T10_handle,) ,) \
            = self._ble.gatts_register_services(_SERVICES)
        self._connections = set()
        # advertise that we are here and what services we provide
        self._payload = advertising_payload(name=name, services=_ADV_SERVICES, appearance=_ADV_APPEARANCE_GENERIC_WEIGHT_SCALE)
        print('Start advertising')
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _, = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _, = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()

    def start(self):
        #log.info('Starting Bluetooth')
        print('Starting Bluetooth')
        self._ble.active(True)

    def stop(self):
        #log.info('Stopping Bluetooth')
        print('Stopping Bluetooth')
        self._ble.active(False)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def set_battery_level(self, level=0, notify=False): 
        """
        Level in [%]
        Data is uint8
        Resolution: 1
        """
        self._ble.gatts_write(self._BS_handle, struct.pack('<B', int(level)))
        print('Write BS: ', struct.pack('<B', int(level)))
        if notify:
            for conn_handle in self._connections:   # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._BS_handle)     
                print('Notify BS handle: ',self._BS_handle)   

    def set_weight(self, weight=0.0, notify=False): 
        """
        weight in [kg]
        Data is uint16
        Resolution: 0.005
        """
        print(' Weight', weight)
        self._ble.gatts_write(self._WS_handle, struct.pack('<h', int(weight/0.005)))
        print(' Write WS: ', struct.pack('<h', int(weight/0.005)))
        if notify:
            for conn_handle in self._connections:   # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._WS_handle)

    def set_humidity(self, humidity=0.0, notify=False): 
        """
        humidity in [%]
        Data is uint16. 
        Resolution: 0.01.
        """
        self._ble.gatts_write(self._ES_HUM_handle, struct.pack('<h', int(humidity/0.01)))
        print('  Write ES HUM: ', struct.pack('<h', int(humidity/0.01)))
        if notify:
            for conn_handle in self._connections:   # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._ES_HUM_handle)

    def set_temperature(self, temperature=0.0, notify=False): 
        """
        temperature in [°C]
        Data is sint16. 
        Resolution of 0.01.
        """
        self._ble.gatts_write(self._ES_TEMP_handle, struct.pack('<h', int(temperature/0.01)))
        print('   Write ES TEMP: ', struct.pack('<h', int(temperature/0.01)))
        if notify:
            for conn_handle in self._connections:   # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._ES_TEMP_handle)

    def set_comb_gap_temperature(self, temperature_list=None, notify=False): 
        """
        temperature in [°C]
        Data is sint16. 
        Resolution of 0.01.
        """
        if temperature_list is None:
            temperature_list = []
        
        for i in range(0, len(temperature_list)):
            if i == 0:
                self._ble.gatts_write(self._TB_T01_handle, struct.pack('<h', int(temperature_list[0]/0.01)))
                print('    Write TB TEMP01: ', struct.pack('<h', int(temperature_list[0]/0.01)))
            if i == 1:
                self._ble.gatts_write(self._TB_T02_handle, struct.pack('<h', int(temperature_list[1]/0.01)))
                print('    Write TB TEMP02: ', struct.pack('<h', int(temperature_list[1]/0.01)))
            if i == 2:
                self._ble.gatts_write(self._TB_T03_handle, struct.pack('<h', int(temperature_list[2]/0.01)))
                print('    Write TB TEMP03: ', struct.pack('<h', int(temperature_list[2]/0.01)))
            if i == 3:
                self._ble.gatts_write(self._TB_T04_handle, struct.pack('<h', int(temperature_list[3]/0.01)))
                print('    Write TB TEMP04: ', struct.pack('<h', int(temperature_list[3]/0.01)))
            if i == 4:
                self._ble.gatts_write(self._TB_T05_handle, struct.pack('<h', int(temperature_list[4]/0.01)))
                print('    Write TB TEMP05: ', struct.pack('<h', int(temperature_list[4]/0.01)))
            if i == 5:
                self._ble.gatts_write(self._TB_T06_handle, struct.pack('<h', int(temperature_list[5]/0.01)))
                print('    Write TB TEMP06: ', struct.pack('<h', int(temperature_list[5]/0.01)))
            if i == 6:
                self._ble.gatts_write(self._TB_T07_handle, struct.pack('<h', int(temperature_list[6]/0.01)))
                print('    Write TB TEMP07: ', struct.pack('<h', int(temperature_list[6]/0.01)))
            if i == 7:
                self._ble.gatts_write(self._TB_T08_handle, struct.pack('<h', int(temperature_list[7]/0.01)))
                print('    Write TB TEMP08: ', struct.pack('<h', int(temperature_list[7]/0.01)))
            if i == 8:
                self._ble.gatts_write(self._TB_T09_handle, struct.pack('<h', int(temperature_list[8]/0.01)))
                print('    Write TB TEMP09: ', struct.pack('<h', int(temperature_list[8]/0.01)))
            if i == 9:
                self._ble.gatts_write(self._TB_T10_handle, struct.pack('<h', int(temperature_list[9]/0.01)))
                print('    Write TB TEMP10: ', struct.pack('<h', int(temperature_list[9]/0.01)))

    def set_name(self, name='Hiveeyes', notify=False): 
        """
        Data is utf8s. 
        """
        pass
        #self._ble.gatts_write(self._ES_TEMP_handle, struct.pack('<h', int(temperature/0.01)))
        if notify:
            for conn_handle in self._connections:   # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._ES_TEMP_handle)

    def set_appearance(self, appearance=3200, notify=False): 
        """
        Data is ? 
        """
        pass
        #self._ble.gatts_write(self._ES_TEMP_handle, struct.pack('<h', int(temperature/0.01)))
        if notify:
            for conn_handle in self._connections:   # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._ES_TEMP_handle)

def demo():
    ble = BLE()
    ble32 = BluetoothApiESP32(ble)

    bat = 54
    kg = 32.1
    hum = 65.4
    temp = 23.4
    temp_gap = [12.3,45.6]

    i = 0

    while True:
        # Write every second, notify every x seconds.
        i += 1
        if i % 3 == 0:
            ble32.set_battery_level(int(bat), notify=False)
            print('bat: ',bat)
        if i % 5 == 0:    
            ble32.set_weight(kg, notify=False)
            print(' kg: ',kg)
        if i % 7 == 0:
            ble32.set_humidity(hum, notify=False)
            print('  hum: ',hum)
        if i % 11 == 0:
            ble32.set_temperature(temp, notify=False)
            print('   temp: ',temp)
        if i % 13 == 0:
            ble32.set_comb_gap_temperature(temp_gap, notify=False)
            print('    temp gap: ',temp)

        # Random walk 
        #bat += int(random.uniform(-1, 1))
        #kg += random.uniform(-0.5, 0.5)
        #hum += random.uniform(-0.5, 0.5)
        #temp += random.uniform(-0.5, 0.5)
        time.sleep_ms(1000)

if __name__ == '__main__':
    demo()