import re
from urllib import request, parse, error
from datetime import datetime, timezone
import pytz
import tzlocal

def prepare_img_urls(loc_names):

    img_url_pattern = re.compile('current1\.jpg\?rid=(\d+)')

    url = 'https://www.farsondigitalwatercams.com/locations/render_event_response'

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    for loc_name in loc_names:

        parameters = {
            'id': loc_name,
            'child': 'live_image',
            'si': 'false',
            'source': 'tabs',
            'type': 'ajax_child_display'
        }
        request_data = parse.urlencode(parameters)
        url = url + '?' + request_data
        req = request.Request(url, headers=headers, method='GET')

        try:
            response = request.urlopen(req)
            html = response.read()
            html = html.decode("utf-8")
            print(html)
            match_res = img_url_pattern.findall(html)
            print(match_res)

        except error.HTTPError as e:
            print(e.reason)


def get_imgs(loc_names, st_id, interval, image_n):

    img_urls = prepare_img_urls(loc_names)
    return

    url = 'https://www.farsondigitalwatercams.com/locations/render_event_response'
    
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    parameters = {
        'id': location_name,
        'child': 'live_image',
        'si': 'false',
        'source': 'tabs',
        'type': 'ajax_child_display'
    }
    request_data = parse.urlencode(parameters)
    url = url + '?' + request_data
    req = request.Request(url, headers=headers, method='GET')

    try:
        response = request.urlopen(req)
        html = response.read()
        html = html.decode("utf-8")
        print(html)
        
        # current1.jpg\?rid=(\d+)

        # file = open('D:/ISIC/structure/LIST-' + str(dataset_id) + '.json', 'w')
        # file.write(html)
        # file.close()

    except error.HTTPError as e:
        print(e.reason)


if __name__ == '__main__':

    london_tz = pytz.timezone('Europe/London')
    local_tz = tzlocal.get_localzone()

    time_st_london = london_tz.localize(datetime(2019, 8, 1, 22, 21, 0)) # London time
    time_st_local = time_st_london.astimezone(local_tz)
    timestamp_st_local = time_st_local.timestamp()

    print('Start Getting Image List.')
    print('\tAt London time:', time_st_london)
    print('\tAt local time:', time_st_local)

    print(timestamp_st_local)

    loc_names = ['turriff', 'bainbridge-yorebridge', 'henley-on-thames']
    get_imgs(loc_names=loc_names, st_id=int(timestamp_st_local), interval=10, image_n=100)

    print('Finished.')