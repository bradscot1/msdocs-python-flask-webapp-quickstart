from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
import csv
import json


app = Flask(__name__)
app.config['REFERRER_POLICY'] = 'no-referrer-when-downgrade'


def read_csv_file(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    return data


@app.route('/hello', methods=['POST'])
def hello():
    zip_code = request.form.get('zip')
    if not zip_code:
        return redirect(url_for('index'))

    # Read data from CSV file
    data = read_csv_file(os.path.join(app.static_folder, 'data', 'outage_mock.csv'))

    graph_data = {}
    for row in data:
        season, reason, total_cost = row['Season'], row['Reason'], float(row['Total_Cost'])
        if reason not in graph_data:
            graph_data[reason] = {
                'Spring': 0,
                'Summer': 0,
                'Fall': 0,
                'Winter': 0
            }
        graph_data[reason][season] += total_cost

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


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()



