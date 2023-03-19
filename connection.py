import pyodbc
from flask import request

# Replace the placeholders with your own values
server = 'quotechies.database.windows.net'
database = 'quotechies-db'
username = 'bscott129@quotechies'
password = 'hackathon10!'
driver= '{ODBC Driver 17 for SQL Server}'


# Create the connection string
connection_string = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password


# Set up the connection
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

cnxn = pyodbc.connect(connection_string)

# Query the database
cursor = cnxn.cursor()


# Insert zip code and session ID into session table
zip_code = request.form.get('zip')
session_id = request.cookies.get('session_id')
cursor.execute(f"INSERT INTO session (zip_code, session_id) VALUES ('{zip_code}', '{session_id}')")

# Commit the transaction
cnxn.commit()

# Close the database connection
cnxn.close()

