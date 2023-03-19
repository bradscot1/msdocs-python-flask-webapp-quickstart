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

cursor.execute(f"SELECT * FROM session")

results = cursor.fetchall()
for row in results:
    print(row)
# Commit the transaction
cursor.close()

# Close the database connection
conn.close()

