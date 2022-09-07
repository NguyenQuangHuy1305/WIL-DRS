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
                beach INTEGER,
                boatTrips INTEGER,
                indigenousTourism INTEGER,
                museumsAndCultureCentres INTEGER,
                nationalParksAndProtectedAreas INTEGER,
                rural INTEGER,
                themeParks INTEGER,
                urbanSightseeing INTEGER,
                waterActivities INTEGER,
                winterActivities INTEGER,
                architectureAndHeritage INTEGER,
                arts INTEGER,
                culture INTEGER,
                excitement INTEGER,
                gastronomy INTEGER,
                nature INTEGER,
                relaxation INTEGER,
                religiousTourism INTEGER,
                sports INTEGER)
				'''

# Creating the table into our
# database
cursor.execute(create_table)

# Opening the person-records.csv file
file = open('Destination_tags_sum.csv')

# Reading the contents of the
# person-records.csv file
contents = csv.reader(file)
next(contents)

# SQL query to insert data into the
# person table
insert_records = "INSERT INTO location (name, beach, boatTrips, indigenousTourism, museumsAndCultureCentres, nationalParksAndProtectedAreas, rural, themeParks, urbanSightseeing, waterActivities, winterActivities, architectureAndHeritage, arts, culture, excitement, gastronomy, nature, relaxation, religiousTourism, sports) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

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
