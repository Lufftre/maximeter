import asyncio
import json
import websockets
from db import insert_data
last_seen_data = {
    "stw": 0,
    "sog": 0,
    "tws": 0,
    "aws": 0,
    "twa": 0,
    "awa": 0,
    "lat": 0,
    "lon": 0
}

connections = [None] * 16


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 2598)

    while True:
        data = await reader.read(2048)
        try:
            data_json = json.loads(data)
        except Exception:
            continue

        try:
            pgn = data_json.get("pgn")
            if pgn == 130306:
                ref, speed, angle = parse_wind(data_json)
                if ref == "Apparent":
                    last_seen_data["awa"] = angle
                    last_seen_data["aws"] = speed
                else:
                    last_seen_data["twa"] = angle
                    last_seen_data["tws"] = speed

            elif pgn == 128259:
                speed = parse_speed(data_json)
                last_seen_data["stw"] = speed
                insert_data(last_seen_data)
            for ws in connections:
                if not ws:
                    continue
                await ws.send(json.dumps(last_seen_data))
        except Exception as error:
            print(error)

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


def parse_wind(data):
    ref = data["fields"]["Reference"]["name"]
    speed = data["fields"]["Wind Speed"]
    angle = data["fields"]["Wind Angle"]
    return ref, speed, angle


def parse_speed(data):
    speed = data["fields"]["Speed Water Referenced"]
    return speed


async def handler(websocket):
    sid = connections.index(None)
    connections[sid] = websocket
    print("client connected", websocket)
    while True:
        try:
            await websocket.recv()
        except websockets.ConnectionClosed:
            print("Terminated")
            connections[sid] = None
            break


async def main():
    await websockets.serve(handler, "", 8001)
    await tcp_echo_client()
    await asyncio.Future()


asyncio.run(main())
