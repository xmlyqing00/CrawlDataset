import json
import time
import os
from datetime import datetime
from dateutil import parser
from urllib import request, parse, error

from send_email import Email


filter_out = [(3,6), (4,3), (4,4), (4,10), (4,11), (4,17), (4,18), (2,21)]
idea_days = [(2, 25)]

def download_page(month):
    url = f'https://api.parkwhiz.com/v4/venues/478490/events/?fields=%3Adefault%2Csite_url%2Cavailability%2Cvenue%3Atimezone&page={month-1}&sort=start_time&zoom=pw%3Avenue'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    # request_data = parse.urlencode(parameters)
    req = request.Request(url, headers=headers, method='GET')
    time_slots = []

    try:
        response = request.urlopen(req)
        html = response.read()
        html = html.decode("utf-8")
        data = json.loads(html)

        for item in data:
            if item['availability']['available'] == 0:
                continue
            
            time_st = parser.parse(item['start_time'])
            weekday = time_st.weekday()
            if (time_st.month, time_st.day) in filter_out:
                continue
            
            if (time_st.month, time_st.day) in idea_days:
                time_slots.append((time_st, weekday, time_st.hour))

            if weekday in [5, 6] and time_st.hour < 12:
                time_slots.append((time_st, weekday, time_st.hour))

    except error.HTTPError as e:
        print(e.reason)


    return time_slots

if __name__ == '__main__':

    duration = 3  # seconds
    freq = 440  # Hz

    email_server = Email()
    last_email = None
    sleep_interval = 60

    while True:

        time.sleep(sleep_interval)

        time_slots = download_page(month=2)
        time_slots += download_page(month=3)
        time_slots += download_page(month=4)

        if len(time_slots) == 0:
            continue
        else:
            print(datetime.now(), time_slots)

        content = str(time_slots)
        if last_email and content == last_email:
            continue
        
        os.system(f'play -nq -t alsa synth {duration} sine {freq}')

        email_server.send('Eldora parking', content)
        last_email = content
