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
    else:
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

        colors = ['red', 'blue', 'green', 'orange', 'purple']
        x_labels = ['Spring', 'Summer', 'Fall', 'Winter']
        datasets = []
        for index, (reason, values) in enumerate(graph_data.items()):
            data = [values['Spring'], values['Summer'], values['Fall'], values['Winter']]
            datasets.append({
                'label': reason,
                'data': data,
                'borderColor': colors[index % len(colors)],
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
                },
                'title': {
                    'display': True,
                    'text': 'Increased Energy Costs in your Region',
                    'fontColor': 'white',
                    'fontSize': 28
                }
            }
        }
        chart_json = json.dumps(chart_data)

        # Total Blackout Duration
        duration_data = {
            'Spring': 0,
            'Summer': 0,
            'Fall': 0,
            'Winter': 0
        }
        data = read_csv_file(os.path.join(app.static_folder, 'data', 'outage_mock.csv'))
        for row in data:
            season, duration = row['Season'], int(row['Blackout_Duration'])
            duration_data[season] += duration

        duration_datasets = [{
            'label': '',
            'data': [duration_data['Spring'], duration_data['Summer'], duration_data['Fall'], duration_data['Winter']],
            'backgroundColor': colors[:len(duration_data)],
        }]
        duration_chart_data = {
            'type': 'bar',
            'data': {
                'labels': x_labels,
                'datasets': duration_datasets
            },
            'options': {
                'scales': {
                    'yAxes': [{
                        'ticks': {
                            'beginAtZero': True
                        },
                        'scaleLabel': {
                            'display': True,
                            'labelString': 'Hours',
                            'fontColor': 'white',
                            'fontSize': 24
                        }
                    }],
                    'xAxes': [{
                        'ticks': {
                            'fontColor': 'white',
                            'fontSize': 16
                        },
                        'gridLines': {
                            'color': 'white'
                        }
                    }]
                },
                'title': {
                    'display': True,
                    'text': 'Total Blackout Hours by Season',
                    'fontColor': 'white',
                    'fontSize': 28
                },
                'legend': {
                    'display': False
                }
            }
        }
        duration_chart_json = json.dumps(duration_chart_data)

    return render_template('hello.html', zip=zip_code, chart_data=chart_json, duration_data=duration_chart_json)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
