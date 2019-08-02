import os
import re
import pytz
import tzlocal

from urllib import request, parse, error
from datetime import datetime, timezone
from threading import Timer

interval = 10
dataset_folder = 'Ship01/Dataset/FarsonWater'

img_lefts = []
img_urls = []
img_ids = []
loc_paths = []

def prepare_img_urls(loc_names):

    img_url_pattern = re.compile('src="(.+)\?rid=(\d+)"')

    common_url = 'https://www.farsondigitalwatercams.com/locations/render_event_response'
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
        url = common_url + '?' + request_data
        req = request.Request(url, headers=headers, method='GET')

        try:
            response = request.urlopen(req)
            html = response.read()
            html = html.decode("utf-8")
            match_res = img_url_pattern.findall(html)

            if len(match_res) > 0:
                img_url, img_id = match_res[0]
                img_urls.append(img_url)
                img_ids.append(int(img_id))
            else:
                print('Unable to fetch initial data at:', loc_name)

        except error.HTTPError as e:
            print(e.reason)


def fetch_img(loc_id):
    
    if img_lefts[loc_id] > 0:
        img_lefts[loc_id] -= 1
        t = Timer(interval, fetch_img, [loc_id])
        t.start()
    
    headers = {
        'User-Agent': 'Mozilla/5.0',

    }
    img_url = img_urls[loc_id] + '?ref=' + str(img_ids[loc_id])

    req = request.Request(img_url, headers=headers, method='GET')
    try:
        response = request.urlopen(req, timeout=10)
        html = response.read()
        file = open('D:/ISIC/data/' + dataset_name + '/' + image_info['name'] + '.jpg', 'wb')
        file.write(html)
        file.close()

    except Exception as e:
        print(e)
        image_count -= 1


def batch_fetch_imgs(loc_names, img_n, st_id=None):

    print('Fetch images in the following %d locations:' % (len(loc_names)))
    print('\t', loc_names)

    if not os.path.exists(dataset_folder):
        print('Create dataset folder at:', dataset_folder)
        os.makedirs(dataset_folder)

    prepare_img_urls(loc_names)
    print(img_urls, img_ids)

    for i in range(len(loc_names)):
        
        loc_paths[i] = os.path.join(dataset_folder, loc_names[i])
        if not os.path.exists(loc_paths[i]):
            print('Create location folder at:', loc_paths[i])
            os.makedirs(loc_paths[i])
            
        img_lefts[i] = img_n

        t = Timer(interval, fetch_img, [i])
        t.start()
    

if __name__ == '__main__':

    london_tz = pytz.timezone('Europe/London')
    local_tz = tzlocal.get_localzone()

    time_st_london = london_tz.localize(datetime(2019, 8, 1, 22, 21, 0)) # London time
    time_st_local = time_st_london.astimezone(local_tz)
    timestamp_st_local = int(time_st_local.timestamp())

    print('Start Getting Image List.')
    print('\t At London time:', time_st_london)
    print('\t At local time:', time_st_local)

    loc_names = ['turriff', 'bainbridge-yorebridge', 'henley-on-thames']
    batch_fetch_imgs(loc_names=loc_names, img_n=100)

    print('Finished.')