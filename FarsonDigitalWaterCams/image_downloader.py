import os
import re
import pytz
import tzlocal

from urllib import request, parse, error
from datetime import datetime, timezone
from threading import Timer


class ImageDownloader:

    def __init__(self, loc_names, dataset_folder, img_n, time_st, interval=10):
        
        # Properties
        self.loc_names = loc_names
        self.dataset_folder = dataset_folder
        self.img_n = img_n
        self.interval = interval

        # Computation data
        self.img_lefts = []
        self.img_urls = []
        self.img_ids = []
        self.loc_paths = []
        self.referers = []

        # Timezone
        self.tz_london = pytz.timezone('Europe/London')
        self.tz_local = tzlocal.get_localzone()

        time_st_london = self.tz_london.localize(time_st)
        time_st_local = time_st_london.astimezone(self.tz_local)
        self.timestamp_st_local = int(time_st_local.timestamp())

        print('Start Getting Image List.')
        print('\t At London time:', time_st_london)
        print('\t At local time:', time_st_local)

        print('Fetch images in the following %d locations in the UK:' % (len(loc_names)))
        print('\t', self.loc_names)
        print('')

        if not os.path.exists(dataset_folder):
            print('Create dataset folder at:', dataset_folder)
            os.makedirs(dataset_folder)
        
        for i in range(len(self.loc_names)):
            
            loc_path = os.path.join(self.dataset_folder, self.loc_names[i])
            self.loc_paths.append(loc_path)
            if not os.path.exists(loc_path):
                print('Create location folder at:', loc_path)
                os.makedirs(loc_path)

            self.img_lefts.append(self.img_n)

        print('')

    def __del__(self):
        print('Farson Image Downloader ends.')

    def prepare_img_urls(self):

        img_url_pattern = re.compile('src="(.+)\?rid=(\d+)"')

        common_url = 'https://www.farsondigitalwatercams.com/locations/render_event_response'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }

        for loc_name in self.loc_names:

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
            self.referers.append(url)

            try:
                response = request.urlopen(req)
                html = response.read()
                html = html.decode("utf-8")
                match_res = img_url_pattern.findall(html)

                if len(match_res) > 0:
                    img_url, img_id = match_res[0]
                    self.img_urls.append(img_url)
                    self.img_ids.append(int(img_id))
                else:
                    print('Unable to fetch initial data at:', loc_name)

            except error.HTTPError as e:
                print(e.reason)


    def fetch_img(self, loc_id):
        
        self.img_lefts[loc_id] -= 1
        if self.img_lefts[loc_id] > 0:
            t = Timer(self.interval, self.fetch_img, [loc_id])
            t.start()
        
        if self.img_ids[loc_id] < self.timestamp_st_local:
            self.img_lefts[loc_id] += 1
            print('Sleep... left:', self.img_lefts[loc_id], '\tcur ts:', self.img_ids[loc_id], 'target ts:', self.timestamp_st_local)
            
        else:
            headers = {
                'Referer': self.referers[loc_id],
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            }
            img_url = self.img_urls[loc_id] + '?ref=' + str(self.img_ids[loc_id])

            time_local = datetime.fromtimestamp(self.img_ids[loc_id])
            time_london = self.tz_local.localize(time_local).astimezone(self.tz_london)

            print('Fetch %s, left: %d.' % (self.loc_names[loc_id], self.img_lefts[loc_id]), '\tLondon time:', time_london)

            req = request.Request(img_url, headers=headers, method='GET')
            try:
                response = request.urlopen(req, timeout=3)
                html = response.read()

                file_name = time_london.strftime('%Y-%m-%d-%H-%M-%S')
                img_path = os.path.join(self.loc_paths[loc_id], file_name + '.jpg')
                file = open(img_path, 'wb')
                file.write(html)
                file.close()

            except Exception as e:
                print(e)

        self.img_ids[loc_id] += self.interval


    def batch_fetch_imgs(self):

        self.prepare_img_urls()
        print(self.img_urls, self.img_ids)

        for i in range(len(self.loc_names)):
            self.fetch_img(i)
    

