# Import required modules
import csv
import sqlite3

# Connecting to the geeks database
connection = sqlite3.connect('database.db')

# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()

# Table Definition
create_table = '''CREATE TABLE rating(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user INTEGER,
				location_id INTEGER,
				location_rating INTEGER,

				beach INTEGER,
				boat_trips INTEGER,
				indigenous_tourism INTEGER,
				museums_and_culture_centres INTEGER,
				national_parks_and_protected_areas INTEGER,
				rural INTEGER,
				theme_parks INTEGER,
				urban_sightseeing INTEGER,
				water_activities INTEGER,
				winter_activities INTEGER,
				architecture_and_heritage INTEGER,
				arts INTEGER,
				culture INTEGER,
				excitement INTEGER,
				gastronomy INTEGER,
				nature INTEGER,
				relaxation INTEGER,
				religious_tourism INTEGER,
				sports INTEGER)
				'''

# Creating the table into our
# database
cursor.execute(create_table)

# Opening the person-records.csv file
file = open('initiateRating.csv', encoding="utf8")

# Reading the contents of the
# person-records.csv file
contents = csv.reader(file)
next(contents)

# SQL query to insert data into the
# person table
insert_records = "INSERT INTO rating (user, location_id, location_rating, beach, boat_trips, indigenous_tourism, museums_and_culture_centres, national_parks_and_protected_areas, rural, theme_parks, urban_sightseeing, water_activities, winter_activities, architecture_and_heritage, arts, culture, excitement, gastronomy, nature, relaxation, religious_tourism, sports) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

# Importing the contents of the file
# into our person table
cursor.executemany(insert_records, contents)

# SQL query to retrieve all data from
# the person table To verify that the
# data of the csv file has been successfully
# inserted into the table
select_all = "SELECT * FROM rating"
rows = cursor.execute(select_all).fetchall()

# Output to the console screen
for r in rows:
	print(r)

# Committing the changes
connection.commit()

# closing the database connection
connection.close()
