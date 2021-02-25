import serial
from decode import FDXDecode
import time
from queue import Queue
import datetime
import logging
import random

def read_messages():
    with serial.Serial('/dev/ttyACM0') as s:
        while True:
            data = s.read_until(b'\x81')
            try:
                msg = FDXDecode(data)
                if msg:
                    yield msg
            except Exception as error:
                print(error)

def read_messages2():
    try:
        while True:
            time.sleep(0.1)
            yield dict(
                boat_speed=13.2,
                wind_speed=12.2,
                wind_angle=43.2,
            )
    except KeyboardInterrupt:
        pass


def read_messages3(q: Queue):
    try:
        while True:
            time.sleep(0.1)
            q.put(dict(
                time=datetime.datetime.now(),
                boat_speed=random.random() * 10,
                wind_speed=random.random() * 10,
                wind_angle=random.random() * 100,
            ))
    except KeyboardInterrupt:
        pass
