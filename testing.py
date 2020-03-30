import Database

import _sqlite3
import csv

conn = _sqlite3.connect('shopBaseWithExample.db')

curs = conn.cursor()

# INSERT EXAMPLES : place , user , errand , item , items_in_errand, user_accepted_errand, session
try:
    user_insert = "INSERT INTO user (user_id, email, last_name, first_name, postcode, street, house_number, password ) VALUES (?, ?, ?, ?, ?, ?, ? ,?)"

    test_user = (0, 'email_0', 'last_name', 'first_name', '35708', 'street', 0, 'password')
    test_user1 = (1, 'email_1', 'last_name', 'first_name', '57072', 'street', 1, 'password')
    curs.execute(user_insert, test_user)
    curs.execute(user_insert, test_user1)
    print("Insert test_users successful!")

except Exception as insertUserErr:
    print('insertUserErr: ', insertUserErr)

# INSERT ERRAND
try:
    errand_insert = "INSERT INTO errand (errand_id, status, startDate, endDate, postcode, email, phone_number, notice) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    test_errand = (0, 0, '2020-04-01', '2020-05-01', 35708, 'albino@gmail.com', '0420818169', 'Hit me!')
    test_errand2 = (1, 0, '2020-05-01', '2020-06-01', 35708, 'hasher@gmail.com', '0420818169', 'Leegma!')
    curs.execute(errand_insert, test_errand)
    curs.execute(errand_insert, test_errand2)
    print('Insert test_errands successful!')

except Exception as insertErrandErr:
    print('insertErrandErr: ', insertErrandErr)

# INSERT ITEMS INTO ERRAND

try:
    items_in_errand_insert = "INSERT INTO items_in_errand (item_id, amount, errand_id) VALUES (?, ?, ?)"

    test_items_in_errand00 = (1, 10, 0)
    test_items_in_errand01 = (2, 3, 0)
    test_items_in_errand02 = (3, 4, 0)
    test_items_in_errand03 = (5, 6, 0)
    test_items_in_errand10 = (1, 3, 1)
    test_items_in_errand11 = (2, 24, 1)
    test_items_in_errand12 = (3, 41, 1)
    test_items_in_errand13 = (5, 6, 1)

    curs.execute(items_in_errand_insert, test_items_in_errand00)
    curs.execute(items_in_errand_insert, test_items_in_errand01)
    curs.execute(items_in_errand_insert, test_items_in_errand02)
    curs.execute(items_in_errand_insert, test_items_in_errand03)
    curs.execute(items_in_errand_insert, test_items_in_errand10)
    curs.execute(items_in_errand_insert, test_items_in_errand11)
    curs.execute(items_in_errand_insert, test_items_in_errand12)
    curs.execute(items_in_errand_insert, test_items_in_errand13)

    print('Insert test_items_in_errand successful!')

except Exception as insertItemsInErrandErr:
    print('insertItemsInErrandErr: ', insertItemsInErrandErr)

# INSERT USER_ACCEPTED_ERRAND
try:
    user_accepted_errand_insert = "INSERT INTO user_accepted_errand (user_id, errand_id) VALUES (?, ?)"

    test_accepted_errand = (1, 0)

    curs.execute(user_accepted_errand_insert, test_accepted_errand)

    print('Insert user_accepted_errand successful!')

except Exception as insertUserAcceptedErrandErr:
    print('insertUserAcceptedErrandErr: ', insertUserAcceptedErrandErr)

conn.commit()

print(Database.registerUser("test_last", "test_vor", "57072", "street.str", "16a", "testing", "test@test.de"))

ses = Database.login("test@test.de", "testing")
print(ses)

print(Database.makeErrand("57072", "", "0374047772", "notice_me", [{"item_id": 0, "amount": 3},{"item_id": 4, "amount": 3}]))

errands = Database.getAuftraege(ses, 57072)
print(errands)

print(Database.getAuftrag(ses, errands[0]["errand_id"]))

print(Database.takeErrand(ses, errands[0]["errand_id"]))

print(Database.getAuftraege(ses,-1))

Database.logout(ses)

Database.getArtikels()