from urllib import request
from urllib import parse
from urllib import error


def GetImageList(dataset_name, dataset_id, data_limit):

    url = 'https://isic-archive.com/api/v1/image'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    parameters = {
        'limit': data_limit,
        'sort': 'name',
        'sortdir': 1,
        'detail': 'true',
        'datasetId': dataset_id
    }
    request_data = parse.urlencode(parameters)
    url = url + '?' + request_data
    req = request.Request(url, headers=headers, method='GET')

    try:
        response = request.urlopen(req)
        html = response.read()
        html = html.decode("utf-8")
        file = open('D:/ISIC/structure/' + dataset_name + '.json', 'w')
        file.write(html)
        file.close()

    except error.HTTPError as e:
        print(e.reason)

if __name__ == '__main__':
    print('Start Getting Image List.')
    GetImageList(dataset_name='MSK-2', dataset_id='5a2ecc5d1165975c94594284', data_limit=1535)
    print('Finished.')