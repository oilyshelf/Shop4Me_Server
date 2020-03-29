import mysql.connector
import pymysql
import csv

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",

)

mytable = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="shop4me"

)

myDbCursor = mydb.cursor()
myTableCursor = mytable.cursor()

# delete all databases
try:
    myDbCursor.execute("DROP DATABASE IF EXISTS `shop4me`")
except Exception as DropDbError:
    print('DropDbError: ', DropDbError)

# create database shop4me
try:
    myDbCursor.execute('CREATE DATABASE IF NOT EXISTS `shop4me`')
except Exception as CreateDbError:
    print('CreateDbError: ', CreateDbError)

# TODO: create tables, missing foreign keys yet
try:
    myTableCursor.execute("CREATE TABLE user (user_id INT AUTO_INCREMENT PRIMARY KEY , last_name VARCHAR(255), first_name VARCHAR(255), postcode VARCHAR(255), street VARCHAR(255), house_number INT(255) )")
    myTableCursor.execute("CREATE TABLE place (primary_key INT AUTO_INCREMENT PRIMARY KEY, state VARCHAR(255), city VARCHAR(255), postcode INT(255))")
    myTableCursor.execute("CREATE TABLE item (item_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description VARCHAR(255), price INT(255))")
    myTableCursor.execute("CREATE TABLE errand (errand_id INT AUTO_INCREMENT PRIMARY KEY, postcode VARCHAR(255), email VARCHAR(255), phone_number VARCHAR(255), notice VARCHAR(255))")
    myTableCursor.execute("CREATE TABLE items_in_errand (item_id INT(255), errand_id INT(255))")
    myTableCursor.execute("CREATE TABLE user_accepted_errand (user_id INT(255), errand_id INT(255))")
    myTableCursor.execute("CREATE TABLE session (session_id INT AUTO_INCREMENT PRIMARY KEY, user_id INTEGER(255), FOREIGN KEY(user_id) REFERENCES user(user_id))")
except Exception as CantCreateTableErr:
    print('CantCreateTableErr: ', CantCreateTableErr)

# read places.csv

"""with open("places.csv", newline='', encoding='utf-8-sig') as csvfile:

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


# import Arrays to table "places"

try:
    sql = "INSERT INTO `shop4me`.`place`(`state`, `city`, `postcode`) VALUES(%s, %s, %s)"

    for x in range(0, len(primary_key)):
        myTableCursor.execute(sql, (state[x], city[x], postcode[x]))
        print(state[x])

except Exception as fillTablePlacesErr:
    print('fillTablePlacesErr: ', fillTablePlacesErr)
"""

mytable.commit()


# SHOW TABLES
myTableCursor.execute("SHOW TABLES")

for x in myTableCursor:
    print(x)
