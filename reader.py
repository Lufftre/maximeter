from socketcan import CanRawSocket
import can
import functools
import asyncio
import time
import db as db
from polar import performance
s = CanRawSocket('can0')


def run_in_executor(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, lambda: f(*args, **kwargs))

    return inner


@run_in_executor
def read_frame():
    frame = s.recv()
    return frame


@run_in_executor
def write_frame(frame):
    s.send(frame)


sow = 0
tws = 0
twa = 0

async def reader():
    global sow, tws, twa
    with db.Session() as session:
        while True:
            frame = await read_frame()
            src, pgn, prio = can.from_can_id(frame.can_id)
            if pgn == 128259:
                print(pgn, frame.data)
                db.insert_speed(session, frame.data)
                # db.insert_speed(session, int(time.time()) & 0xf)

            elif pgn == 130306:
                print(pgn, frame.data)
                db.insert_wind(session, frame.data)
                # db.insert_wind(frame)


async def writer():
    while True:
        p = performance(tws, twa, sow)
        frame = can.polar_performance(p)
        write_frame(frame)
        # print('write')
        await asyncio.sleep(0.5)


async def iso_claimer():
    frame = can.iso_address_claim()
    t = time.time()
    while True:
        write_frame(frame)
        print('iso', time.time() - t)
        t = time.time()
        await asyncio.sleep(3)


async def main():
    await reader()

if __name__ == '__main__':
    # asyncio.run_forever(main())
    loop = asyncio.get_event_loop()
    loop.create_task(reader())
    loop.create_task(iso_claimer())
    loop.create_task(writer())
    loop.run_forever()
    loop.close()
