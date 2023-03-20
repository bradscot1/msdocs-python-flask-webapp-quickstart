from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import io
import base64




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




        # Create the connection string
        connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"




        # Set up the connection
        engine = create_engine(connection_string)
        conn = engine.connect()




        # Insert zip code
        query = text("INSERT INTO session2 (zip_code) VALUES (:zip)")
        conn.execute(query, zip=zip)




        # Query the data for the graph
        query = text("""
            SELECT Season, Reason, AVG(Avg_Price)
            FROM weather_incidents
            GROUP BY Season, Reason
            ORDER BY
                CASE Season
                    WHEN 'Spring' THEN 1
                    WHEN 'Summer' THEN 2
                    WHEN 'Fall' THEN 3
                    WHEN 'Winter' THEN 4
                END
        """)
        data = conn.execute(query)




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
        conn.close()




        # Create a line chart
        fig, ax = plt.subplots()
        for reason, values in graph_data.items():
            x = ['Spring', 'Summer', 'Fall', 'Winter']
            y = [values['Spring'], values['Summer'], values['Fall'], values['Winter']]
            ax.plot(x, y, label=reason)
        ax.set_xlabel('Season')
        ax.set_ylabel('Average Price')
        ax.set_title('Energy Surge Costs Due to Outages by Season')
        ax.legend()




        # Encode the image as a base64 string
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        image_string = base64.b64encode(buffer.getvalue()).decode()




        # Render the template with the image embedded
        return render_template('hello.html', zip=zip, image_string=image_string)




    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(debug=True)





