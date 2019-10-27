from network import Bluetooth
import time
import struct

bluetooth = Bluetooth()
print('Scanning...')
bluetooth.start_scan(2)    # start scanning with no timeout
time.sleep(2.1)

if not bluetooth.isscanning():
    for adv in bluetooth.get_advertisements():
        name = bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
        if name == 'HEN':
            mac = adv.mac

# org.bluetooth.service.battery_service - BS_BS_INT = 0x180F
# org.bluetooth.characteristic.battery_level_BS_CHAR = (UUID(0x2A19), FLAG_READ | FLAG_NOTIFY,)

# org.bluetooth.service.weight_scale - WS_WS_INT = 0x181D
# org.bluetooth.characteristic.weight_measurement_WS_CHAR = (UUID(0x2A9D), FLAG_READ | FLAG_NOTIFY,)

# org.bluetooth.service.environmental_sensing - ES _ES_INT = 0x181A

            try:
                conn = bluetooth.connect(adv.mac)
                services = conn.services()
                for service in services:
                    time.sleep(0.050)
                    if service.uuid() == 0x180f: 
                        print('Battery service')
                        chars = service.characteristics()
                        for char in chars:
                            if (char.properties() & Bluetooth.PROP_READ):
                                print('char {} value = {}'.format(char.uuid(), char.read()))
                                print('Battery level: ', struct.unpack('<b', char.value())[0])
                    elif service.uuid() == 0x181d:
                        print('Weight scale')
                        chars = service.characteristics()
                        for char in chars:
                            if (char.properties() & Bluetooth.PROP_READ):
                                print('char {} value = {}'.format(char.uuid(), char.read()))
                                print('Weight: ', struct.unpack('<h', char.value())[0]*0.005)
                    elif service.uuid() == 0x181a:
                        print('Environ Sensing')
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
