import asyncio
import json
import random
import websockets
stw = 0
connections = [None] * 16


async def tcp_echo_client():
    global stw
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 2598)

    while True:
        data = await reader.read(2048)
        data_json = json.loads(data)
        if not data:
            break

        pgn = data_json.get("pgn")
        if pgn == 128259:
            stw = data_json["fields"]["Speed Water Referenced"] + random.random()*3
            for ws in connections:
                if not ws:
                    continue
                await ws.send(json.dumps({"stw": stw}))
            print(stw)

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


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
