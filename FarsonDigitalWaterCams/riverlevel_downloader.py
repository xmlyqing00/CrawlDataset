import os
import re
import pytz
import tzlocal

from urllib import request, parse, error
from datetime import datetime, timezone
from threading import Timer


class RiverlevelDownloader:

    def __init__(self, loc_names, dataset_folder, img_n, time_st, interval=10):
        
        # Constants
        delay = 3600

        # Properties
        self.loc_names = loc_names
        self.dataset_folder = dataset_folder
        self.img_n = img_n
        self.interval = interval

        # Computation data
        self.loc_paths = []
        self.img_urls = []

        # Timezone
        self.tz_london = pytz.timezone('Europe/London')
        self.tz_local = tzlocal.get_localzone()

        time_st_london = self.tz_london.localize(time_st)
        time_st_local = time_st_london.astimezone(self.tz_local)
        timestamp_st_local = int(time_st_local.timestamp())
        timestamp_ed_local = timestamp_st_local + interval * img_n
        self.timestamp_st_riverlevel = timestamp_ed_local + delay

        time_ed_local = datetime.fromtimestamp(timestamp_ed_local)
        time_ed_london = self.tz_local.localize(time_ed_local).astimezone(self.tz_london)
        file_suffix = time_ed_london.strftime('%Y-%m-%d-%H-%M-%S')

        print('Get river level dataset.')
        print('\t At London time:', time_ed_london)
        print('\t At local time:', time_ed_local)
        print('Start crawling at local timestamp:', self.timestamp_st_riverlevel)

        print('Fetch images in the following %d locations in the UK:' % (len(loc_names)))
        print('\t', loc_names)
        print('')

        if not os.path.exists(dataset_folder):
            print('Create dataset folder at:', dataset_folder)
            os.makedirs(dataset_folder)
        
        
        for i in range(len(self.loc_names)):
            
            loc_path = os.path.join(self.dataset_folder, self.loc_names[i] + '_' + file_suffix + '.json')
            self.loc_paths.append(loc_path)

            url = 'https://watercams.azureedge.net/locations/%s/stations?timeframe=86400&parameters=RiverLevel,Rainfall&forecast=0' % (self.loc_names[i])
            self.img_urls.append(url)

        print('')

    def __del__(self):
        print('Farson Riverlevel Downloader ends.')

    def fetch_riverlevel(self, loc_id):
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        }
        img_url = self.img_urls[loc_id]
        req = request.Request(img_url, headers=headers, method='GET')

        print('Fetch %s' % (self.loc_names[loc_id]))

        try:
            response = request.urlopen(req, timeout=3)
            html = response.read()

            img_path = os.path.join(self.loc_paths[loc_id])
            file = open(img_path, 'wb')
            file.write(html)
            file.close()

        except Exception as e:
            print(e)



    def batch_fetch_riverlevels(self):

        cur_ts = int(datetime.now().timestamp())
        sleep_time = max(0, self.timestamp_st_riverlevel - cur_ts)
        print('Cur ts:', cur_ts, 'Sleep time (s):', sleep_time)

        for i in range(len(self.loc_names)):
            t = Timer(sleep_time, self.fetch_riverlevel, [i])
            t.start()
    
