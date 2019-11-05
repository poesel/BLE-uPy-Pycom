# org.bluetooth.service.battery_service - BS_BS_INT = 0x180F
# org.bluetooth.characteristic.battery_level_BS_CHAR = (UUID(0x2A19), FLAG_READ | FLAG_NOTIFY,)
# org.bluetooth.service.weight_scale - WS_WS_INT = 0x181D
# org.bluetooth.characteristic.weight_measurement_WS_CHAR = (UUID(0x2A9D), FLAG_READ | FLAG_NOTIFY,)
# org.bluetooth.service.environmental_sensing - ES _ES_INT = 0x181A

from network import Bluetooth
import time
import struct

print('Create BT')
bluetooth = Bluetooth()
print('Scanning...')
bluetooth.start_scan(2)    # start scanning with no timeout
time.sleep(2.1)

if not bluetooth.isscanning():
    for adv in bluetooth.get_advertisements():
        name = bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
        if name == 'HEN':
            mac = adv.mac

            try:
                print('Connecting to HEN')
                conn = bluetooth.connect(adv.mac)
                time.sleep(0.05)
                services = conn.services()
                for service in services:
                    time.sleep(0.050)
                    #print('Service: ',service.uuid())
                    #print('Chars: ',service.characteristics())
                    uuid = service.uuid()
                    if type(uuid) == bytes:
                        #uuid_str = UUIDbytes2UUIDstring(uuid)
                        pass

                    if service.uuid() == 0x180F0: 
                        print('Battery service')
                        chars = service.characteristics()
                        for char in chars:
                            if (char.properties() & Bluetooth.PROP_READ):
                                print('char {} value = {}'.format(char.uuid(), char.read()))
                                print('Battery level: ', struct.unpack('<b', char.value())[0])
                    elif uuid == 0x181D0:
                        print('Weight scale')
                        chars = service.characteristics()
                        for char in chars:
                            if (char.properties() & Bluetooth.PROP_READ):
                                print('char {} value = {}'.format(char.uuid(), char.read()))
                                print('Weight: ', struct.unpack('<h', char.value())[0]*0.005)
                    elif uuid == 0x181A0:
                        print('Environ Sensing')
                        chars = service.characteristics()
                        for char in chars:
                            if (char.properties() & Bluetooth.PROP_READ):
                                print('char {} value = {}'.format(char.uuid(), char.read()))
                                if char.uuid() == 0x2A6F:  # humidity
                                    print('Humidity: ', struct.unpack('<h', char.value())[0]*0.01)
                                elif char.uuid() == 0x2A6E:    # temperature
                                    print('Temperature: ', struct.unpack('<h', char.value())[0]*0.01)
                    elif uuid_str == '04500100-39fd-49ec-b565-b5d6dc31b6ae':
                        print('Temp gap')
                        chars = service.characteristics()
                        for char in chars:
                            if (char.properties() & Bluetooth.PROP_READ):
                                print('char {} value = {}'.format(char.uuid(), char.read()))


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


                    #if type(service.uuid()) == bytes:
                    #    print('fReading chars from service = {}'.format(service.uuid()))
                    #else:
                    #    print('Reading chars from service = %x' % service.uuid())
                    #chars = service.characteristics()
                    #for char in chars:
                    #    if (char.properties() & Bluetooth.PROP_READ):
                    #        print('char {} value = {}'.format(char.uuid(), char.read()))
                conn.disconnect()
            except:
                pass

        #print('Name: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))
        #print('Appearance: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_APPEARANCE))


            #print('ADV_FLAG: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_FLAG))
            #print('ADV_16SRV_PART: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_16SRV_PART))
            ##print('ADV_T16SRV_CMPL: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_T16SRV_CMPL))
            #print('ADV_32SRV_PART: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_32SRV_PART))
            #print('ADV_32SRV_CMPL: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_32SRV_CMPL))
            #print('ADV_128SRV_PART: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_128SRV_PART))
            #print('ADV_128SRV_CMPL: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_128SRV_CMPL))
            #print('ADV_NAME_SHORT: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_SHORT))
            ##print('ADV_NAME_CMPL: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))
            #print('ADV_TX_PWR: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_TX_PWR))
            #print('ADV_DEV_CLASS: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_DEV_CLASS))
            #print('ADV_SERVICE_DATA: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_SERVICE_DATA))
            #print('ADV_APPEARANCE: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_APPEARANCE))
            #print('ADV_ADV_INT: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_ADV_INT))
            #print('ADV_32SERVICE_DATA: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_32SERVICE_DATA))
            #print('ADV_128SERVICE_DATA: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_128SERVICE_DATA))
            #print('ADV_MANUFACTURER_DATA: ',bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA))
            #print(adv)

def uuid2bytes(uuid):
    # https://forum.pycom.io/topic/530/working-with-uuid/2
    import binascii
    uuid = uuid.encode().replace(b'-', b'')
    tmp = binascii.unhexlify(uuid)
    return bytes(reversed(tmp))

def UUIDbytes2UUIDstring(uuid):
    '''
    reverses the bytes of uuid and converts them to a properly formatted UUID string
    '''
    from ubinascii import hexlify
    tmp = str(hexlify(bytes(reversed(uuid))))[2:34]
    return tmp[0:8]+'-'+tmp[8:12]+'-'+tmp[12:16]+'-'+tmp[16:20]+'-'+tmp[20:32]
