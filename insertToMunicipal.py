# Import required modules
import csv
import sqlite3

# Connecting to the geeks database
connection = sqlite3.connect('database.db')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# Table Definition
create_table = '''CREATE TABLE municipal(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				state TEXT NOT NULL,
                name TEXT NOT NULL)
				'''

# Creating the table into our
# database
cursor.execute(create_table)

# Opening the person-records.csv file
file = open('State.csv', encoding="utf8")

# Reading the contents of the
# person-records.csv file
contents = csv.reader(file)
next(contents)

# SQL query to insert data into the
# person table
insert_records = "INSERT INTO municipal (state, name) VALUES(?, ?)"

# Importing the contents of the file
# into our person table
cursor.executemany(insert_records, contents)

# SQL query to retrieve all data from
# the person table To verify that the
# data of the csv file has been successfully
# inserted into the table
select_all = "SELECT * FROM municipal"
rows = cursor.execute(select_all).fetchall()

# Output to the console screen
for r in rows:
	print(r)

# Committing the changes
connection.commit()

# closing the database connection
connection.close()
