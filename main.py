"""import asyncio
import json
import websockets
from Listener import listener

USERS = set()


async def register(websocket):
    USERS.add(websocket)


async def unregister(websocket):
    USERS.remove(websocket)


async def server(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:

        async for message in websocket:
            data = json.loads(message)
            await listener(data, websocket)

    finally:
        await unregister(websocket)


start_server = websockets.serve(server, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()"""

