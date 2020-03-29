import websockets
import asyncio
import json
import logging
import Database

logging.basicConfig()


async def notify_one(websocket, message):
    await websocket.send(message)


async def listener(dict, websocket):
    if dict["action"] == "login":
        await loginLis(websocket, dict["email"], dict["password"])
    elif dict["action"] == "register":
        await registerLis(websocket, dict["last_name"], dict["first_name"], dict["postcode"], dict["street"],
                          dict["house_number"], dict["password"], dict["email"])
    elif dict["action"] == "logout":
        await logoutLis(websocket, dict["sessionID"])
    elif dict["action"] == "getItems":
        await getItemsLis(websocket)
    elif dict["action"] == "getErrands":
        await getErrendsLis(websocket, dict["postcode"], dict["sessionID"])
    elif dict["action"] == "getErrand":
        await getErrendLis(websocket, dict["sessionID"], dict["errandID"])
    elif dict["action"] == "takeErrand":
        await takeErrendLis(websocket, dict["sessionID"], dict["errandID"])
    elif dict["action"] == "makeErrand":
        await makeErrandLis(websocket, dict["postcode"], dict["email"], dict["phone_number"], dict["notice"],
                            dict["items"])

    else:
        print("No such Action %s found" % (dict["action"]))
        logging.error("unsupported event: {}", dict)


async def loginLis(websocket, email, password):
    sesId = Database.login(email, password)
    if sesId != -1:
        message = json.dumps({"action": "login", "Success": True, "SessionID": sesId})
    else:
        message = json.dumps(
            {"action": "login", "Success": False, "Error": "Email or Password wrong or you have no Account"})

    await websocket.send(message)


async def registerLis(websocket, last_name, first_name, postcode, street, house_number, password, email):
    if Database.registerUser(last_name, first_name, postcode, street, house_number, password, email):
        success = True
    else:
        success = False
    message = json.dumps({"action": "register", "Success": success})
    await websocket.send(message)


async def logoutLis(websocket, sessionID):
    suc = Database.logout(sessionID)
    await websocket.send(json.dumps({"action": "logout", "Success": suc}))


async def getItemsLis(websocket):
    await websocket.send(json.dumps({"action": "getItems", "items": Database.getArtikels()}))


async def getErrendsLis(websocket, plz, sessionID):
    errs = Database.getAuftraege(sessionID, plz)
    if errs != -1:
        message = {"action": "getErrands", "Success": True, "errands": errs}
    else:
        message = {"action": "getErrands", "Success": False, "Error": "No Errands found"}
    await websocket.send(json.dumps(message))


async def getErrendLis(websocket, sessionID, errandID):
    message = {"action": "getErrand", "Success": True, "errand": Database.getAuftrag(sessionID, errandID)}
    await websocket.send(json.dumps(message))


async def takeErrendLis(websocket, sessionID, errandID):
    succ = Database.takeErrand(sessionID, errandID)
    await websocket.send(json.dumps({"action": "takeErrand", "Success": succ}))


async def makeErrandLis(websocket, postcode, email, phone_number, notice, articleList):
    succ = Database.makeErrand(postcode, email, phone_number, notice, articleList)
    await websocket.send(json.dumps({"action": "makeErrand", "Success": succ}))
