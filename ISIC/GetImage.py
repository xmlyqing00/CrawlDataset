from urllib import request
from urllib import error
import json
import os


def GetImage(dataset_name, start_id=0):

    if not os.path.exists('D:/ISIC/data/' + dataset_name):
        os.mkdir('D:/ISIC/data/' + dataset_name)

    width = 256
    height = 256

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    file = open('D:/ISIC/structure/' + dataset_name + '.json', 'r')
    image_list = json.load(file)
    file.close()

    image_count = 0

    while image_count < len(image_list):

        if image_count < start_id:
            image_count += 1
            continue

        image_info = image_list[image_count]
        image_count += 1

        try:
            diagnosis = image_info['meta']['clinical']['diagnosis']
        except KeyError:
            diagnosis = None

        try:
            acquisition = image_info['meta']['acquisition']['image_type']
        except KeyError:
            acquisition = None

        print(image_count, image_info['_id'], image_info['name'], diagnosis, acquisition)

        if diagnosis is None or diagnosis not in ['melanoma', 'nevus', 'seborrheic keratosis']:
            print('Diagnosis is not in the preset set.')
            continue

        if acquisition is None or acquisition != 'dermoscopic':
            print('Acquisition is not dermoscopic.')
            continue

        url = 'https://isic-archive.com/api/v1/image/{0}/thumbnail?width={1}&height={2}'.format(
            image_info['_id'],
            width,
            height
        )

        req = request.Request(url, headers=headers, method='GET')

        try:
            response = request.urlopen(req, timeout=10)
            html = response.read()
            file = open('D:/ISIC/data/' + dataset_name + '/' + image_info['name'] + '.jpg', 'wb')
            file.write(html)
            file.close()

        except Exception as e:
            print(e)
            image_count -= 1


if __name__ == '__main__':
    # dataset_attr = [
    #     {'name': 'MSK-1'},
    #     {'name': 'MSK-2'},
    #     {'name': 'MSK-3'},
    #     {'name': 'MSK-4'},
    #     {'name': 'MSK-5'},
    #     {'name': 'SONIC'},
    #     {'name': 'UDA-1'},
    #     {'name': 'UDA-2'}
    # ]

    for i in range(0, 14):

        dataset_name = 'LIST-' + str(i)
        print('Start Getting Images. ', dataset_name)
        GetImage(dataset_name=dataset_name)

    print('Finished.')