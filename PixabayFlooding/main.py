

import json
from tqdm import tqdm
import time
import os
from datetime import datetime
from dateutil import parser
from urllib import request, parse, error

def download(query: str, page: int = 1):

    url = f'https://pixabay.com/api/'
    params = {
        'key': '23950615-814a58d226eb4f14b57f33bc0',
        'q': query,
        'page': page,
        'image_type': 'photo',
        # 'safesearch': 'true',
        'per_page': 200
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    request_data = parse.urlencode(params)
    url += '?' + request_data
    print(url)
    req = request.Request(url, headers=headers, method='GET')
    try:
        response = request.urlopen(req)
        html = response.read()
        html = html.decode('utf-8')
        return_data = json.loads(html)

    except error.HTTPError as e:
        print(e.reason)
        return

    cnt_new = 0
    cnt_old = 0
    for i, hit in enumerate(tqdm(return_data['hits'])):

        if f'{hit["id"]}.jpg' in already_download_list:
            cnt_old += 1
            continue
        else:
            cnt_new += 1

        req = request.Request(hit['largeImageURL'], headers=headers, method='GET')
        response = request.urlopen(req, timeout=3)
        html = response.read()

        img_path = os.path.join(out_dir, f'{hit["id"]}.jpg')
        file = open(img_path, 'wb')
        file.write(html)
        file.close()

    print(f'New: {cnt_new}, Old: {cnt_old}')

    # print(return_data)


if __name__ == '__main__':

    query = 'flooding water'
    out_dir = '/Ship01/Dataset/VOS/water/JPEGImages/flooding_pixabay/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    already_download_list = os.listdir(out_dir)


    for i in range(1, 30):
        download(query, i)
        time.sleep(10)
