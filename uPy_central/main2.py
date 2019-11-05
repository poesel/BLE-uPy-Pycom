# org.bluetooth.service.battery_service - BS_BS_INT = 0x180F
# org.bluetooth.characteristic.battery_level_BS_CHAR = (UUID(0x2A19), FLAG_READ | FLAG_NOTIFY,)
# org.bluetooth.service.weight_scale - WS_WS_INT = 0x181D
# org.bluetooth.characteristic.weight_measurement_WS_CHAR = (UUID(0x2A9D), FLAG_READ | FLAG_NOTIFY,)
# org.bluetooth.service.environmental_sensing - ES _ES_INT = 0x181A

from ubluetooth import BLE, UUID, FLAG_NOTIFY, FLAG_READ, FLAG_WRITE
import time
import struct

from micropython import const
_IRQ_SCAN_RESULT                     = const(1 << 4)
_IRQ_SCAN_COMPLETE                   = const(1 << 5)
_IRQ_PERIPHERAL_CONNECT              = const(1 << 6)
_IRQ_PERIPHERAL_DISCONNECT           = const(1 << 7)
_IRQ_GATTC_SERVICE_RESULT            = const(1 << 8)
_IRQ_GATTC_CHARACTERISTIC_RESULT     = const(1 << 9)
_IRQ_GATTC_DESCRIPTOR_RESULT         = const(1 << 10)
_IRQ_GATTC_READ_RESULT               = const(1 << 11)
_IRQ_GATTC_WRITE_STATUS              = const(1 << 12)
_IRQ_GATTC_NOTIFY                    = const(1 << 13)


class BLECentralESP32:
    """
    """

    def __init__(self, ble):
        """
        Start BLE
        """
        self._ble = ble
        self._ble.active(True)
        #self._ble.irq(handler=self._irq)
        #self._connections = set()

    def _scan(self, number=0, duration_ms=0):
        """
        Scan for BLE advertisements until <number> have been reached or timeout
        number: number of nodes to find
        duration_ms:    '0' for indefinite scan, 'None' to stop
        """
        pass

    def _gather(self, targets):
        """
        connect to <targets> and gather data
        """
        pass

    def _irq(self, event, data):
        """ handle BLE events """
        if event == _IRQ_SCAN_RESULT:
            # A single scan result.
            addr_type, addr, connectable, rssi, adv_data = data
            print('Scan result: ',data)
        elif event == _IRQ_SCAN_COMPLETE:
            # Scan duration finished or manually stopped.
            pass
        elif event == _IRQ_PERIPHERAL_CONNECT:
            # A successful gap_connect().
            conn_handle, addr_type, addr = data
            self._connections.add(conn_handle)
        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            # Connected peripheral has disconnected.
            conn_handle, addr_type, addr = data
            self._connections.remove(conn_handle)
        elif event == _IRQ_GATTC_SERVICE_RESULT:
            # Called for each service found by gattc_discover_services().
            conn_handle, start_handle, end_handle, uuid = data
        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            # Called for each characteristic found by gattc_discover_services().
            conn_handle, def_handle, value_handle, properties, uuid = data
        elif event == _IRQ_GATTC_DESCRIPTOR_RESULT:
            # Called for each descriptor found by gattc_discover_descriptors().
            conn_handle, dsc_handle, uuid = data
        elif event == _IRQ_GATTC_READ_RESULT:
            # A gattc_read() has completed.
            conn_handle, value_handle, char_data = data
        elif event == _IRQ_GATTC_WRITE_STATUS:
            # A gattc_write() has completed.
            conn_handle, value_handle, status = data
        elif event == _IRQ_GATTC_NOTIFY:
            # A peripheral has sent a notify request.
            conn_handle, value_handle, notify_data = data

    def _start(self):
        #log.info('Starting Bluetooth')
        print('Starting Bluetooth')
        self._ble.active(True)

    def _stop(self):
        #log.info('Stopping Bluetooth')
        print('Stopping Bluetooth')
        self._ble.active(False)


#            try:
#                print('Connecting to HEN')
#                conn = bluetooth.connect(adv.mac)
#                services = conn.services()
#                for service in services:
#                    time.sleep(0.050)
#                    #print('Service: ',service.uuid())
#                    #print('Chars: ',service.characteristics())
#                    uuid = service.uuid()
#                    if type(uuid) == bytes:
#                        #uuid_str = UUIDbytes2UUIDstring(uuid)
#                        pass

#                    if service.uuid() == 0x180F0: 
#                        print('Battery service')
#                        chars = service.characteristics()
#                        for char in chars:
#                            if (char.properties() & Bluetooth.PROP_READ):
#                                print('char {} value = {}'.format(char.uuid(), char.read()))
#                                print('Battery level: ', struct.unpack('<b', char.value())[0])
#                    elif uuid == 0x181D0:
#                        print('Weight scale')
#                        chars = service.characteristics()
#                        for char in chars:
#                            if (char.properties() & Bluetooth.PROP_READ):
#                                print('char {} value = {}'.format(char.uuid(), char.read()))
#                                print('Weight: ', struct.unpack('<h', char.value())[0]*0.005)
#                    elif uuid == 0x181A0:
#                        print('Environ Sensing')
#                        chars = service.characteristics()
#                        for char in chars:
#                            if (char.properties() & Bluetooth.PROP_READ):
#                                print('char {} value = {}'.format(char.uuid(), char.read()))
#                                if char.uuid() == 0x2A6F:  # humidity
#                                    print('Humidity: ', struct.unpack('<h', char.value())[0]*0.01)
#                                elif char.uuid() == 0x2A6E:    # temperature
#                                    print('Temperature: ', struct.unpack('<h', char.value())[0]*0.01)
#                    elif uuid_str == '04500100-39fd-49ec-b565-b5d6dc31b6ae':
#                        print('Temp gap')
#                        chars = service.characteristics()
#                        for char in chars:
#                            if (char.properties() & Bluetooth.PROP_READ):
#                                print('char {} value = {}'.format(char.uuid(), char.read()))


# Hiveeyes (HE) service for temperature sensors inside the brood box (TB)
#_HE_TB_UUID = UUID('04500100-39fd-49ec-b565-b5d6dc31b6ae')
# characteristics: 10 temperature sensors
#_HE_TB_CHAR_T01 = (UUID('04500101-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
#_HE_TB_CHAR_T02 = (UUID('04500102-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
#_HE_TB_CHAR_T03 = (UUID('04500103-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
#_HE_TB_CHAR_T04 = (UUID('04500104-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
#_HE_TB_CHAR_T05 = (UUID('04500105-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
#_HE_TB_CHAR_T06 = (UUID('04500106-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
#_HE_TB_CHAR_T07 = (UUID('04500107-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
#_HE_TB_CHAR_T08 = (UUID('04500108-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
#_HE_TB_CHAR_T09 = (UUID('04500109-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)
#_HE_TB_CHAR_T10 = (UUID('04500110-39fd-49ec-b565-b5d6dc31b6ae'), FLAG_READ | FLAG_NOTIFY,)


def uuid2bytes(uuid):
    # https://forum.pycom.io/topic/530/working-with-uuid/2
    import binascii
    uuid = uuid.encode().replace(b'-', b'')
    tmp = binascii.unhexlify(uuid)
    return bytes(reversed(tmp))

def UUIDbytes2UUIDstring(uuid):
    """
    reverses the bytes of uuid and converts them to a properly formatted UUID string
    """
    from ubinascii import hexlify
    tmp = str(hexlify(bytes(reversed(uuid))))[2:34]
    return tmp[0:8]+'-'+tmp[8:12]+'-'+tmp[12:16]+'-'+tmp[16:20]+'-'+tmp[20:32]

def demo():
    ble = BLE
    ble32 = BLECentralESP32(ble)
    print('Start scan')
    #ble32.gap_scan(2000)
    

if __name__ == '__main__':
    demo()    