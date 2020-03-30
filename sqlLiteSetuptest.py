import _sqlite3
import csv
#doesnt need to be run all the changes here are safed
conn = _sqlite3.connect('shopBaseWithExample.db')

curs = conn.cursor()

curs.execute("CREATE TABLE place (primary_key INT AUTO_INCREMENT , state VARCHAR(255), city VARCHAR(255), postcode VARCHAR(255), primary key (primary_key))")
curs.execute(
    "CREATE TABLE user (user_id INTEGER PRIMARY KEY AUTOINCREMENT , email VARCHAR(255) UNIQUE , last_name VARCHAR(255), first_name VARCHAR(255), postcode VARCHAR(255), street VARCHAR(255), house_number VARCHAR(255), password VARCHAR(255), Foreign key (postcode) References place(postcode) )")

curs.execute(
    "CREATE TABLE item (item_id INT AUTO_INCREMENT , item_name VARCHAR(255), description VARCHAR(255), price REAL(255), primary key (item_id))")

curs.execute(
    "CREATE TABLE errand (errand_id INTEGER PRIMARY KEY AUTOINCREMENT , status INT default 0, startDate DATE , endDate DATE, postcode VARCHAR(255), email VARCHAR(255), phone_number VARCHAR(255), notice VARCHAR(255))")

curs.execute("CREATE TABLE items_in_errand (item_id INT(255), amount INT(255), errand_id INT(255), primary key(item_id,errand_id) Foreign key (item_id) references item(item_id), foreign key (errand_id) references errand(errand_id))")
curs.execute("CREATE TABLE user_accepted_errand (user_id INT(255), errand_id INT(255), primary key(user_id,errand_id), Foreign key (user_id) references item(user_id), foreign key (errand_id) references errand(errand_id))")
curs.execute(
    "CREATE TABLE session (session_id VARCHAR(255), user_id INTEGER(255),primary key (session_id), FOREIGN KEY(user_id) REFERENCES user(user_id))")


with open("Database/places.csv", newline='', encoding='utf-8-sig') as csvfile:

    readCSV = csv.reader(csvfile, delimiter=';')

    primary_key = []
    postcode = []
    city = []
    state = []
    community = []
    latitude = []
    longitude = []

    next(readCSV)

    for row in readCSV:

        primary_key.append(row[0])
        postcode.append(row[1])
        city.append(row[2])
        state.append(row[3])
        community.append(row[4])
        latitude.append(row[5])
        longitude.append(row[6])

sql = "INSERT INTO place(primary_key, state, city, postcode) VALUES( {}, '{}', '{}', {})"

for x in range(0, len(primary_key)):
    temp = sql.format(primary_key[x], state[x], city[x], postcode[x])
    print(temp)
    curs.execute(temp)

with open("Database/itemlist.csv", newline='', encoding='utf-8-sig') as csvfile1:

    readCSV = csv.reader(csvfile1, delimiter=';')

    item_id = []
    item_name = []
    description = []
    price = []

    next(readCSV)

    for row in readCSV:

        item_id.append(row[0])
        item_name.append(row[1])
        description.append(row[2])
        price.append(row[3])

sql = "INSERT INTO item(item_id, item_name, description, price) VALUES({}, '{}', '{}', {})"

for x in range(0, len(item_id)):
    tempItem = sql.format(item_id[x], item_name[x], description[x], price[x])
    print(tempItem)
    curs.execute(tempItem)


curs.execute("Select state from place")

print(curs.fetchall())

conn.commit()

conn.close()
