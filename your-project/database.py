import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'zomato'

TABLES = {}

TABLES['restaurants'] = (
	"CREATE TABLE IF NOT EXISTS `restaurants` ("
	"	`ID` int PRIMARY KEY AUTO_INCREMENT,"
	"	`name` varchar(20) NOT NULL,"
	"	`cost_for_two` int NOT NULL,"
	"	`neighborhood` varchar(20) NOT NULL,"
	"	`type` varchar(20) NOT NULL,"
	"	`avg_rating` float NOT NULL,"
	"	`#_of_ratings` int NOT NULL"
	") ENGINE=InnoDB")

TABLES['infos'] = (
	"CREATE TABLE IF NOT EXISTS `infos` ("
	"	`ID` int PRIMARY KEY AUTO_INCREMENT,"
	"	`name` varchar(20) NOT NULL"
	") ENGINE=InnoDB")

TABLES['cuisines'] = (
	"CREATE TABLE IF NOT EXISTS `cuisines` ("
	"	`ID` int PRIMARY KEY AUTO_INCREMENT,"
	"	`name` varchar(20) NOT NULL"
	") ENGINE=InnoDB")

try:
	cnx = mysql.connector.connect(user='root', password='v3r0na1989', host='localhost', database=DB_NAME)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

cursor = cnx.cursor()

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cursor.close()
cnx.close()