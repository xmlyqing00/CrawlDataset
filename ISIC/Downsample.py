from PIL import Image
import json
import os


def DownsampleImage(dataset_name, start_id=0):

    if not os.path.exists('D:/ISIC/downsample/' + dataset_name):
        os.mkdir('D:/ISIC/downsample/' + dataset_name)

    if not os.path.exists('D:/ISIC/downsample/' + dataset_name + '/256/'):
        os.mkdir('D:/ISIC/downsample/' + dataset_name + '/256/')

    if not os.path.exists('D:/ISIC/downsample/' + dataset_name + '/100/'):
        os.mkdir('D:/ISIC/downsample/' + dataset_name + '/100/')

    file = open('D:/ISIC/structure/' + dataset_name + '.json', 'r')
    image_list = json.load(file)
    file.close()

    image_count = 0
    dataset_path = 'D:/ISIC/data/' + dataset_name + '/'
    downsample_path = 'D:/ISIC/downsample/' + dataset_name + '/'

    height_100 = 75
    height_256 = 192

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

        img0 = Image.open(dataset_path + image_info['_id'] + '.jpg')

        file = open(downsample_path + '256/' + image_info['_id'] + '.txt', 'w')
        file.write(diagnosis + '\n')

        img = img0.resize(size=(256, height_256), resample=Image.BICUBIC)
        pixels_mat = img.load()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                file.write(str(x) + ' ' + str(y) + ' ')
                for k in range(3):
                    file.write(str(pixels_mat[x,y][k]) + ' ')
                file.write('\n')
        file.close()

        file = open(downsample_path + '100/' + image_info['_id'] + '.txt', 'w')
        file.write(diagnosis + '\n')

        img = img0.resize(size=(100, height_100), resample=Image.BICUBIC)
        pixels_mat = img.load()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                file.write(str(x) + ' ' + str(y) + ' ')
                for k in range(3):
                    file.write(str(pixels_mat[x,y][k]) + ' ')
                file.write('\n')
        file.close()


if __name__ == '__main__':
    dataset_attr = [
        {'name': 'MSK-1'},
        {'name': 'MSK-2'},
        {'name': 'MSK-3'},
        {'name': 'MSK-4'},
        {'name': 'MSK-5'},
        {'name': 'SONIC'},
        {'name': 'UDA-1'},
        {'name': 'UDA-2'}
    ]

    for i in range(0, len(dataset_attr)):

        print('Downsample Images.', dataset_attr[i]['name'])
        DownsampleImage(dataset_name=dataset_attr[i]['name'])

    print('Finished.')