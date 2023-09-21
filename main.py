import socket
import json
# import asyncio
# import websockets

HOST = "127.0.0.1"
PORT = 2598
outfile = "maxi.log"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def parse_json(data):
    json_data = json.loads(data)
    # timestamp = json_data["timestamp"]
    if json_data["pgn"] == 130306:
        # ws = json_data["fields"]["Wind Speed"]
        # kts = ws * 1.94
        # wa = json_data["fields"]["Wind Angle"]
        # wref = json_data["fields"]["Reference"]["name"]
        # print(f"{kts:05.2f} kt {wa:05.1f}° {wref}")
        print(json_data)
        with open(outfile, 'ab') as f:
            f.write((data))
    
    elif json_data["pgn"] == 128259:
        # stw = json_data["fields"]["Speed Water Referenced"]
        # kts = stw * 1.94
        # print(f"{kts:05.2f} kt")
        print(json_data)
        with open(outfile, 'ab') as f:
            f.write((data))
    


# async def handler(websocket):
#     while True:
#         message = await websocket.recv()
#         await websocket.send(message)
#         print(message)


# async def main():
#     async with websockets.serve(handler, "", 8001):
#         await asyncio.Future()  # run forever


# asyncio.run(main())

while True:
    data = s.recv(1024)
    if not data:
        continue

    try:
        parse_json(data)
    except Exception as error:
        print(error, data)



