# Import required modules
import csv
import sqlite3

# Connecting to the geeks database
connection = sqlite3.connect('database.db')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# Table Definition
create_table = '''CREATE TABLE location(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
                urban INTEGER,
                rural INTEGER,
                canyonvalleys INTEGER,
                mountain INTEGER,
                water INTEGER,
                beach INTEGER,
                summer INTEGER,
                winter INTEGER,
                nature INTEGER,
                park INTEGER,
                wildlife INTEGER,
                relax INTEGER,
                entertainment INTEGER,
                nightlife INTEGER,
                ethnic INTEGER,
                culture INTEGER,
                festival INTEGER,
                gastronomy INTEGER,
                religion INTEGER,
                sports INTEGER,
                adventure INTEGER,
                fishing INTEGER)
				'''

# Creating the table into our
# database
cursor.execute(create_table)

# Opening the person-records.csv file
file = open('test.csv')

# Reading the contents of the
# person-records.csv file
contents = csv.reader(file)

# SQL query to insert data into the
# person table
insert_records = "INSERT INTO location (name, urban, rural, canyonvalleys, mountain, water, beach, summer, winter, nature, park, wildlife, relax, entertainment, nightlife, ethnic, culture, festival, gastronomy, religion, sports, adventure, fishing) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

# Importing the contents of the file
# into our person table
cursor.executemany(insert_records, contents)

# SQL query to retrieve all data from
# the person table To verify that the
# data of the csv file has been successfully
# inserted into the table
select_all = "SELECT * FROM location"
rows = cursor.execute(select_all).fetchall()

# Output to the console screen
for r in rows:
	print(r)

# Committing the changes
connection.commit()

# closing the database connection
connection.close()
