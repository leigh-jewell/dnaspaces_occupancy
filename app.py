from flask import Flask, render_template, request
import requests
import json
from datetime import datetime
from datetime import datetime as dt
from activate import process_activation

app = Flask(__name__)


def get_location(event):
    location = "UNKNOWN"
    try:
        location = ">".join(
            (event['deviceCounts']['location']['parent']['parent']['name'],
             event['deviceCounts']['location']['parent']['name'],
             event['deviceCounts']['location']['name']))
    except KeyError as e:
        print(f"get_location(): ERROR: KeyError {e} when trying to extract location from {event}.")
    return location


@app.route('/', methods=['GET'])
def get_home_page():
    return render_template('index.html', api_key="", device_count=[], total_events=0, event_count=0,
                           max_events=100, sample_time=10)


@app.route('/activate', methods=['POST'])
def activate_app():
    api_key = ""
    if request.form['token']:
        token = request.form['token']
        print(f"activate_app(): Got activation token:{token}")
        api_key = process_activation(token)
    else:
        print("activate_app(): Form didn't provide api_key or token.")
    return render_template('index.html', api_key=api_key, device_count=[], total_events=0, event_count=0,
                           max_events=100, sample_time=10)


@app.route('/', methods=['POST'])
def get_device_count_data():
    token = ""
    total_events = 0
    event_count = 0
    max_number_events = 1
    device_count = []
    process_time_secs = 0.0
    max_wait_secs = 20
    print("get_device_count_data():")
    if request.method == 'POST':
        try:
            token = request.form.get('api_key')
            max_wait_secs = int(request.form.get('sample_time'))
            max_number_events = int(request.form.get('max_events'))
            print(f"Got token {token} sample secs {max_wait_secs} total events {max_number_events}")
        except KeyError as e:
            print(f"get_device_count_data: ERROR: unable to get data from submitted form: {e}")
        headers = {'X-API-Key': token}
        # Connect to API
        try:
            stream_api = requests.get('https://partners.dnaspaces.io/api/partners/v1/firehose/events',
                                      stream=True, headers=headers)
            start_time = datetime.now()
            if stream_api.status_code == 200:
                print(f"Successfully connected to Firehose {stream_api.status_code}")
                # Read in an update from Firehose API
                for line in stream_api.iter_lines():
                    event = {}
                    data = json.loads(line)
                    total_events += 1
                    # Only process DEVICE_COUNT events
                    if data['eventType'] == "DEVICE_COUNT":
                        print("!", end="")
                        event_count += 1
                        event['record_timestamp'] = dt.fromtimestamp(data['recordTimestamp'] / 1000)
                        event['location'] = get_location(data)
                        event['associatedCount'] = data['deviceCounts']['associatedCount']
                        event['estimatedProbingCount'] = data['deviceCounts']['estimatedProbingCount']
                        event['probingRandomizedPercentage'] = round(data['deviceCounts']['probingRandomizedPercentage'],4)
                        event['associatedDelta'] = data['deviceCounts']['associatedDelta']
                        event['probingDelta'] = data['deviceCounts']['probingDelta']
                        event['estimatedDensity'] = round(data['deviceCounts']['estimatedDensity'],4)
                        event['estimatedCapacityPercentage'] = round(data['deviceCounts']['estimatedCapacityPercentage'], 2)
                        event['userCount'] = data['deviceCounts']['userCount']
                        event['wirelessUserCount'] = data['deviceCounts']['wirelessUserCount']
                        event['bleTagCount'] = data['deviceCounts']['bleTagCount']
                        device_count.append(event)
                    else:
                        # Print . for all other events
                        print(".", end="")
                    # Only grab updates for a specific period
                    process_time_secs = round((datetime.now() - start_time).total_seconds(), 1)
                    if process_time_secs > max_wait_secs or event_count >= max_number_events:
                        print(f'\nFinished.\nTime taken: {process_time_secs}. Total events: {total_events} '
                              f'Device Count:{event_count}')
                        break
        except requests.exceptions.RequestException as e:
            print(f"get_device_count_data: ERROR: unable to connect to partners.dnaspaces.io: {e}")
    return render_template('index.html', device_count=device_count, time_taken=process_time_secs, api_token=token,
                           max_events=max_number_events, sample_time=max_wait_secs,
                           total_events=total_events, event_count=event_count)


if __name__ == '__main__':
    app.run()
