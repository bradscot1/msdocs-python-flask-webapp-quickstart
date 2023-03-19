from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pyodbc
app = Flask(__name__)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    zip = request.form.get('zip')
    if zip:
        print('Request for hello page received with zip=%s' % zip)

        # Insert the zip code into the database
        server = 'quotechies.database.windows.net'
        database = 'quotechies-db'
        username = 'bscott129@quotechies'
        password = 'hackathon10!'
        driver = '{ODBC Driver 17 for SQL Server}'
        cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()
        cursor.execute("INSERT INTO session (zip_code) VALUES (?)", zip)
        cnxn.commit()


        return render_template('hello.html', zip=zip)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))










