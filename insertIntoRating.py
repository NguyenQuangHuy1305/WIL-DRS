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
				beach_rating INTEGER,
				boatTrips_rating INTEGER,
				indigenousTourism_rating INTEGER,
				museumsAndCultureCentres_rating INTEGER,
				nationalParksAndProtectedAreas_rating INTEGER,
				rural_rating INTEGER,
				themeParks_rating INTEGER,
				urbanSightseeing_rating INTEGER,
				waterActivities_rating INTEGER,
				winterActivities_rating INTEGER,
				architectureAndHeritage_rating INTEGER,
				arts_rating INTEGER,
				culture_rating INTEGER,
				excitement_rating INTEGER,
				gastronomy_rating INTEGER,
				nature_rating INTEGER,
				relaxation_rating INTEGER,
				religiousTourism_rating INTEGER,
				sports_rating INTEGER)
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
insert_records = "INSERT INTO rating (user, location_id, location_rating, beach_rating, boatTrips_rating, indigenousTourism_rating, museumsAndCultureCentres_rating, nationalParksAndProtectedAreas_rating, rural_rating, themeParks_rating, urbanSightseeing_rating, waterActivities_rating, winterActivities_rating, architectureAndHeritage_rating, arts_rating, culture_rating, excitement_rating, gastronomy_rating, nature_rating, relaxation_rating, religiousTourism_rating, sports_rating) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

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
