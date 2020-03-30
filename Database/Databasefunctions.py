import _sqlite3
from .passwordHasher import hash_password, verify_password
from .SessionIDGenerator import generate_session
from datetime import datetime

conn = _sqlite3.connect('shopBaseWithExample.db')

c = conn.cursor()


def registerUser(last_name, first_name, postcode, street, house_number, password, email):
    """regestier a user into database hash password !! and return true when success else false"""
    sql = """ INSERT INTO user (email, last_name, first_name,postcode, street, house_number, password) VALUES ('{}','{}','{}',{},'{}','{}','{}')"""
    hashedPw = hash_password(password)
    success = True
    try:
        with conn:
            sqlFor = sql.format(email, last_name, first_name, postcode, street, house_number, hashedPw)
            print(sqlFor)
            c.execute(sqlFor)
    except Exception as registerUserException:
        print('getUserFromSessionException: ', registerUserException)
        success = False

    return success


def getUserfromSessionID(sessionID):
    """ a function to help find the user_id from the sessionID folder"""
    sql = """ SELECT user_id FROM session WHERE session_id = '{}'"""
    result = None
    try:
        with conn:
            sqlFor = sql.format(sessionID)
            print(sqlFor)
            c.execute(sqlFor)
            result = c.fetchone()[0]
    except Exception as getUserFromSessionException:
        print('getUserFromSessionException: ', getUserFromSessionException)
        result = -1

    return result


def login(email, password):
    """ check if user is in database if in db generate sesid and insert into db  return sessid if success else -1"""
    userInfo = None
    sessionID = None
    sql = """SELECT email, password, user_id FROM user WHERE email = '{}'"""
    try:
        with conn:
            sqlF = sql.format(email)
            print(sqlF)
            c.execute(sqlF)
            userInfo = c.fetchone()
    except Exception as loginException:
        print('loginException: ', loginException)
        return -1

    if verify_password(userInfo[1], password):
        sessionID = generate_session()

        try:
            with conn:
                sql = """ INSERT INTO session VALUES ("{}", {} )"""
                sqlF = sql.format(sessionID, userInfo[2])
                print(sqlF)
                c.execute(sqlF)

        except Exception as verifyPasswordException:
            print('verifyPasswordException: ', verifyPasswordException)
            return -1

    else:
        return -1
    return sessionID


def logout(sessionID):
    """ remove sesID from db return true if success else false"""

    sql = """ DELETE FROM session WHERE session_id = '{}'"""
    try:
        with conn:
            sqlLogout = sql.format(sessionID)
            print(sqlLogout)
            c.execute(sqlLogout)
            print("Logout Successful!")


    except Exception as LogoutException:
        print('LogoutException: ', LogoutException)


def getArtikels():
    """return all articels as a List with dictonary {item_id:, name:}"""
    sqlGetArtikels = """ SELECT item_id, item_name FROM item """
    try:
        with conn:
            print(sqlGetArtikels)
            c.execute(sqlGetArtikels)
            artikelList = c.fetchall()

            artikelz = []
            if artikelList is not None:
                for ass in artikelList:
                    artikelz.append({"item_id": ass[0], "item_name": ass[1]})

                print(artikelz)
                return artikelz

            else:
                return -1

    except Exception as getArtikelsException:
        print('getArtikelsException: ', getArtikelsException)


def getAuftraege(sessionId, plz):
    """check if plz is -1 if -1 return all auftraege assoziated with that user else all auftrege in that plz  return type: list with dictonary {errandid, postcode} else -1"""
    userID = getUserfromSessionID(sessionId)
    errand = None
    if userID != -1:
        if plz == -1:
            sql = """SELECT errand_id, postcode FROM errand NATURAL JOIN user_accepted_errand  WHERE user_id = {}"""
            try:
                with conn:
                    sqlF = sql.format(userID)
                    print(sqlF)
                    c.execute(sqlF)
                    errand = c.fetchall()
            except Exception as myErrandEXP:
                print(myErrandEXP)
                return -1
        else:
            sql = """ SELECT errand_id, postcode FROM errand WHERE postcode = '{}' and status = 0 """
            try:
                with conn:
                    sqlF = sql.format(plz)
                    print(sqlF)
                    c.execute(sqlF)
                    errand = c.fetchall()
            except Exception as ErrandPostcodeEXP:
                print(ErrandPostcodeEXP)
                return -1
    else:
        return -1
    result = []
    if errand is not None:
        for ers in errand:
            result.append({"errand_id": ers[0], "postcode": ers[1]})
        return result
    else:
        return -1


def getAuftrag(sessionid, errend_id):
    """get all the information from that errand as a dictonary"""
    userID = getUserfromSessionID(sessionid)
    res = {}
    if userID != -1:
        sql = """ SELECT * FROM errand WHERE errand_id = {}"""
        try:
            with conn:
                sqlF = sql.format(errend_id)
                print(sqlF)
                c.execute(sqlF)
                temp = c.fetchone()
                sql = """Select amount, item_name, item_id FROM item NATURAL JOIN items_in_errand WHERE errand_id = """ + str(
                    temp[0])
                c.execute(sql)
                tempList = c.fetchall()
        except Exception as getItemEXP:
            print(getItemEXP)
    else:
        return -1
    res["errand_id"] = temp[0]
    res["status"] = temp[1]
    res["startDate"] = temp[2]
    res["endDate"] = temp[3]
    res["postcode"] = temp[4]
    res["email"] = temp[5]
    res["phone_number"] = temp[6]
    res["notice"] = temp[7]
    resList = []
    if tempList is not None:
        for item in tempList:
            resList.append({"amount": item[0], "item_id": item[2], "item_name": item[1]})
    res["itemList"] = resList
    return res


def takeErrand(sessionID, errandID):
    """in db add to user_accepted_errand if errend isnt taken (status = 0), change status from errand to one  return true or false """
    userID = getUserfromSessionID(sessionID)
    if userID != -1:
        try:
            with conn:
                sql = """SELECT status from errand WHERE errand_id = """ + str(errandID)
                print(sql)
                c.execute(sql)
                temp = c.fetchone()[0]
                if temp == 0:
                    sql = """ UPDATE errand SET status = 1 WHERE errand_id = """ + str(errandID)
                    c.execute(sql)
                    sql = """ INSERT INTO user_accepted_errand VALUES ({}, {})"""
                    sqlF = sql.format(userID, errandID)
                    print(sqlF)
                    c.execute(sqlF)
                else:
                    return False
        except Exception as takeErrandEXP:
            print(takeErrandEXP)
            return False
    return True


def makeErrand(postcode, email, phone_number, notice, articleList):
    """ create an new errand with the information status default is 0 / articleList looks like that [{item_id, amount}] add to errand and the from article list in items_in_errand  return bool for success"""
    tempnotice = generate_session()
    date = datetime.now().strftime("%Y-%m-%d")
    sqlcreate = """ INSERT INTO errand (startDate, postcode, email, phone_number,notice) VALUES ('{}', {} ,'{}','{}', '{}') """
    try:
        with conn:
            sqlF = sqlcreate.format(date,postcode,email,phone_number,tempnotice)
            print(sqlF)
            c.execute(sqlF)
            sql = """ SELECT errand_id FROM errand WHERE notice = '"""+tempnotice + "'"
            print(tempnotice)
            print(sql)
            c.execute(sql)
            errand_id = c.fetchone()[0]
            sql = """ UPDATE errand SET notice =  '{}' WHERE errand_id = '{}' """
            sqlF = sql.format(notice,errand_id)
            print(sqlF)
            c.execute(sqlF)
            sql = """INSERT INTO items_in_errand VALUES ({}, {}, {})"""
            for item in articleList:
                sqlF = sql.format(item["item_id"], item["amount"], errand_id)
                print(sqlF)
                c.execute(sqlF)
            return True
    except Exception as makeEXp:
        print(makeEXp)
        return False


