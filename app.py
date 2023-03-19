from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pyodbc
import pandas as pd
app = Flask(__name__)
import matplotlib.pyplot as plt

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def outages():
    zip = request.form.get('zip')thi
    df = pd.read_csv('static/data/outage_mock.csv')
    # Convert Peak_Price_Duration, Blackout_Duration, Peak_price, and Total_Cost columns to numeric types
    df['Peak_Price_Duration'] = pd.to_numeric(df['Peak_Price_Duration'])
    df['Blackout_Duration'] = pd.to_numeric(df['Blackout_Duration'])
    df['Peak_price'] = pd.to_numeric(df['Peak_price'])
    df['Total_Cost'] = pd.to_numeric(df['Total_Cost'])

    # Convert Year column to datetime type
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')

    # Define order of seasons for x-axis labels
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']

    # Create line plot of average price by reason and season
    fig, ax = plt.subplots()
    for reason, group in df.groupby('Reason'):
        group.groupby('Season')['Avg_Price'].mean().loc[season_order].plot(ax=ax, label=reason)

        # Set title and axis labels
    plt.title('Average Price by Reason and Season')
    plt.xlabel('Season')
    plt.ylabel('Average Price')

# Show legend and plot
    plt.legend()
    plt.show()



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


        # Create the connection string
        connection_string = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password


        # Set up the connection
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()


        #cursor.execute("IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='session' and xtype='U') CREATE TABLE session (zip_code varchar(10), session_id varchar(255))")
        cursor.execute("INSERT INTO session2 (zip_code) VALUES (?)", zip)
        conn.commit()


        # Query the data for the graph
        cursor.execute("SELECT Season, Reason, AVG(Avg_Price) FROM weather_incidents GROUP BY Season, Reason ORDER BY CASE Season WHEN 'Spring' THEN 1 WHEN 'Summer' THEN 2 WHEN 'Fall' THEN 3 WHEN 'Winter' THEN 4 END")
        data = cursor.fetchall()


        # Create a dictionary to store the data
        graph_data = {}
        for row in data:
            season, reason, avg_price = row
            if reason not in graph_data:
                graph_data[reason] = {
                    'spring': 0,
                    'summer': 0,
                    'fall': 0,
                    'winter': 0
                }
            graph_data[reason][season.lower()] = avg_price


        # Close the database connection
        cursor.close()
        conn.close()


        return render_template('hello.html', zip=zip, graph_data=graph_data)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))











