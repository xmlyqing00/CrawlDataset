from urllib import request
from urllib import error
import json


def GetImage(dataset_name, start_id=0):

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
        print(image_count, image_info['_id'])
        image_count += 1

        url = 'https://isic-archive.com/api/v1/image/{0}/thumbnail?width={1}&height={2}'.format(
            image_info['_id'],
            width,
            height
        )

        req = request.Request(url, headers=headers, method='GET')

        try:
            response = request.urlopen(req, timeout=10)
            html = response.read()
            file = open('D:/ISIC/data/' + dataset_name + '/' + image_info['_id'] + '.jpg', 'wb')
            file.write(html)
            file.close()

        except Exception as e:
            print(e)
            image_count -= 1


if __name__ == '__main__':
    dataset_name = 'MSK-2'

    print('Start Getting Images.', dataset_name)
    GetImage(dataset_name=dataset_name, start_id=147)
    print('Finished.')