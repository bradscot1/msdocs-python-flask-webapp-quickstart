from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import io
import base64
import traceback
import sys
import json


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello', methods=['POST'])
def hello():
    try:
        zip_code = request.form.get('zip')
        if not zip_code:
            return redirect(url_for('index'))

        server = 'quotechies.database.windows.net'
        database = 'quotechies-db'
        username = 'bscott129@quotechies'
        password = 'hackathon10!'
        driver = '{ODBC Driver 17 for SQL Server}'


        connection_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"
        engine = create_engine(connection_string)
        conn = engine.connect()


        query = text("INSERT INTO session2 (zip_code) VALUES (:zip)")
        conn.execute(query, zip=zip_code)


        query = text("""
            SELECT Season, Reason, AVG(Avg_Price) AS Avg_Price
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


        graph_data = {}
        for row in data:
            season, reason, avg_price = row
            if reason not in graph_data:
                graph_data[reason] = {
                    'Spring': 0,
                    'Summer': 0,
                    'Fall': 0,
                    'Winter': 0
                }
            graph_data[reason][season] = avg_price


        conn.close()


        x_labels = ['Spring', 'Summer', 'Fall', 'Winter']
        datasets = []
        for reason, values in graph_data.items():
            data = [values['Spring'], values['Summer'], values['Fall'], values['Winter']]
            datasets.append({
                'label': reason,
                'data': data,
                'borderColor': 'red',
                'fill': False
            })


        chart_data = {
            'type': 'line',
            'data': {
                'labels': x_labels,
                'datasets': datasets
            },
            'options': {
                'scales': {
                    'yAxes': [{
                        'ticks': {
                            'beginAtZero': True
                        }
                    }]
                }
            }
        }


        chart_json = json.dumps(chart_data)


        return render_template('hello.html', zip=zip_code, chart_data=chart_json)


    except Exception:
        traceback.print_exc(file=sys.stdout)
        return render_template('error.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
