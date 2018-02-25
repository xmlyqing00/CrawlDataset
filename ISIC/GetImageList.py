from urllib import request
from urllib import parse
from urllib import error


limit = 1000

def GetImageList(dataset_id):

    url = 'https://isic-archive.com/api/v1/image'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    parameters = {
        'limit': limit,
        'offset': dataset_id * limit,
        'sort': 'name',
        'sortdir': 1,
        'detail': 'true',
    }
    request_data = parse.urlencode(parameters)
    url = url + '?' + request_data
    req = request.Request(url, headers=headers, method='GET')

    try:
        response = request.urlopen(req)
        html = response.read()
        html = html.decode("utf-8")
        if html == '[]':
            return False
        file = open('D:/ISIC/structure/LIST-' + str(dataset_id) + '.json', 'w')
        file.write(html)
        file.close()

    except error.HTTPError as e:
        print(e.reason)

    return True

if __name__ == '__main__':

    # dataset_attr = [
    #     {'name': 'MSK-1',
    #      'id': '5a2ecc5d1165975c9459427e'},
    #     {'name': 'MSK-2',
    #      'id': '5a2ecc5d1165975c94594284'},
    #     {'name': 'MSK-3',
    #      'id': '5a2ecc5d1165975c9459428a'},
    #     {'name': 'MSK-4',
    #      'id': '5a2ecc5d1165975c9459428e'},
    #     {'name': 'MSK-5',
    #      'id': '5a2ecc5d1165975c94594292'},
    #     {'name': 'SONIC',
    #      'id': '5a2ecc5e1165975c945942a0'},
    #     {'name': 'UDA-1',
    #      'id': '5a2ecc5e1165975c945942a2'},
    #     {'name': 'UDA-2',
    #      'id': '5a2ecc5e1165975c945942a4'}
    # ]

    print('Start Getting Image List.')

    for i in range(0, 100000):

        print(i)

        if not GetImageList(dataset_id=i):
            break

    print('Finished.')