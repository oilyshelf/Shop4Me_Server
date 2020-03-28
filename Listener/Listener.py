import websockets
import asyncio
import json
import logging

logging.basicConfig()


async def notify_one(websocket, message):
    await websocket.send(message)


def listener(dict, websocket):
    if dict["action"] == "login":
        pass
    elif dict["action"] == "register":
        pass
    else:
        print("No such Action %s found" % (dict["action"]))
        logging.error("unsupported event: {}", dict)
