from socketcan import CanFrame
import struct

def to_can_id(pgn, src, dst, prio):
    can_id = src & 0xff | 0x80000000

    pf = (pgn >> 8) & 0xff
    if pf < 240:
        can_id |= (dst & 0xff) << 8
        can_id |= (pgn << 8)
    else:
        can_id |= pgn << 8

    can_id |= prio << 26
    return can_id


def from_can_id(can_id):
    src = 0xff & can_id
    can_id >>= 8

    pgn = 0x3ffff & can_id
    can_id >>= 18

    prio = 0b111 & can_id
    return src, pgn, prio


def iso_address_claim(src=35, dst=255, prio=6):
    can_id = to_can_id(60928, src, dst, prio)
    frame = CanFrame(can_id=can_id, data=b'\xff\xff\xff\xff\xff\xff\xff\xff')
    return frame


def humidity_data(sid, instance, source, actual_humidity, set_humidity):
    data = bytes([sid, instance, source])
    data += (actual_humidity * 250).to_bytes(2, 'little')
    data += (set_humidity * 250).to_bytes(2, 'little')
    data += b'\xff'
    return data


def polar_performance(percentage, src=35, dst=255, prio=3):
    can_id = to_can_id(130313, src, dst, prio)
    data = humidity_data(0xff, 0x01, 0x01, round(percentage), 0)
    frame = CanFrame(can_id=can_id, data=data)
    return frame

