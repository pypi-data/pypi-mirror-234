import time
from robertcommondriver.system.iot.iot_iec104 import IOTIEC104, unpack, IECData, IECPacket


def logging_print(**kwargs):
    print(kwargs)


def test_read():
    dict_config = {'host': '192.168.1.184', 'port': 2404, 'timeout': 4}
    dict_point = {}
    dict_point['iec1'] = {'point_writable': True, 'point_name': 'iec1', 'point_type': 1, 'point_address': 1, 'point_scale': '1'}
    dict_point['iec2'] = {'point_writable': True, 'point_name': 'iec2', 'point_type': 13, 'point_address': 16386, 'point_scale': '1'}

    client = IOTIEC104(configs = dict_config, points= dict_point)
    client.logging(call_logging=logging_print)
    while True:
        try:
            result = client.read(names=list(dict_point.keys()))
            print(result)
        except Exception as e:
            print(f"error: {e.__str__()}")
        time.sleep(1)


def test_parse():
    #r = IOTIEC104.APDU(bytes.fromhex('68 0E 06 00 08 00 64 01 06 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'))
    #r = IOTIEC104.APDU(bytes.fromhex('68 0E 02 00 02 00 01 82 14 00 01 00 01 00 00 01 68 0E 04 00 02 00 64 01 0A 00 01 00 00 00 00 14'))
    r = IOTIEC104.APDU(bytes.fromhex('68 15 16 38 92 00 1E 01 03 00 01 00 7C 00 00 01 D0 84 1A 05 17 08 17'))
    print(r.info())


def test_read1():
    dict_config = {'host': '192.168.1.184', 'port': 2404, 'timeout': 5, 'zongzhao_interval': 0, 'zongzhao_timeout': 30, 'u_test_timeout': 10,  's_interval': 1}
    dict_point = {}
    dict_point['iec1'] = {'point_writable': True, 'point_name': 'iec1', 'point_type': 1, 'point_address': 100, 'point_scale': '1'}
    dict_point['iec2'] = {'point_writable': True, 'point_name': 'iec2', 'point_type': 13, 'point_address': 600, 'point_scale': '1'}

    client = IOTIEC104(configs = dict_config, points= dict_point)
    client.logging(call_logging=logging_print)
    while True:
        try:
            result = client.read(names=list(dict_point.keys()))
            print(result)
        except Exception as e:
            print(f"error: {e.__str__()}")
        time.sleep(5)


def test_frame():
    pkt = IOTIEC104.APDU()
    pkt /= IOTIEC104.APCI(ApduLen=14, Type=0x00, Tx=1, Rx=4)
    pkt /= IOTIEC104.ASDU(Type=101, SQ=0, Cause=6, Num=1, Test=0, OA=0, Addr=1, IOA=[IECData.IOAS[101](IOA=0, QCC=IECPacket.QCC(RQT=0, FRZ=0))])
    print(IOTIEC104().format_bytes(pkt.build()))

    info = IOTIEC104.APDU(bytes.fromhex('68 a3 26 00 04 00 0f 9e 14 00 01 00 a5 65 00 02 00 00 00 00 00 00 00 00 00 13 51 00 00 00 f5 18 00 00 00 00 27 00 00 00 7a 3f 00 00 00 ed 73 00 00 00 9d 27 c7 00 00 00 00 00 00 00 65 12 00 00 00 b3 5d 01 00 00 08 40 f4 01 00 26 41 0b 00 00 5c 00 00 00 00 00 00 00 00 00 18 0a 00 00 00 5f 00 00 00 00 7a b9 7f 00 00 02 db 00 00 00 00 00 00 00 00 4a 9c 9d 00 00 36 01 00 00 00 32 40 89 00 00 01 00 00 00 00 05 00 00 00 00 1d 00 00 00 00 cf 1c 00 00 00 13 29 15 00 00 00 00 00 00 00 8e 00 00 00 00')).info()
    print(info)


def test_dianneng():
    dict_config = {'host': '127.0.0.1', 'port': 2404, 'timeout': 5, 'zongzhao_interval': 0, 'zongzhao_timeout': 30, 'dianneng_interval': 20, 'dianneng_timeout': 10, 'u_test_timeout': 10,  's_interval': 1}
    dict_point = {}
    dict_point['iec1'] = {'point_writable': True, 'point_name': 'iec1', 'point_type': 1, 'point_address': 100, 'point_scale': '1'}
    dict_point['iec2'] = {'point_writable': True, 'point_name': 'iec2', 'point_type': 13, 'point_address': 600, 'point_scale': '1'}
    dict_point['iec3'] = {'point_writable': True, 'point_name': 'iec3', 'point_type': 15, 'point_address': 25633, 'point_scale': '1'}   # 37515
    dict_point['iec4'] = {'point_writable': True, 'point_name': 'iec4', 'point_type': 15, 'point_address': 25697, 'point_scale': '1'}   # 500315

    client = IOTIEC104(configs = dict_config, points= dict_point)
    client.logging(call_logging=logging_print)
    while True:
        try:
            result = client.read(names=list(dict_point.keys()))
            print(result)
        except Exception as e:
            print(f"error: {e.__str__()}")
        time.sleep(5)


test_parse()