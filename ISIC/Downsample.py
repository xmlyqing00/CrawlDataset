from PIL import Image
import json


def DownsampleImage(dataset_name, start_id=0):

    file = open('D:/ISIC/structure/' + dataset_name + '.json', 'r')
    image_list = json.load(file)
    file.close()

    image_count = 0
    dataset_path = 'D:/ISIC/data/' + dataset_name + '/'
    downsample_path = 'D:/ISIC/downsample/' + dataset_name + '/'

    while image_count < len(image_list):

        if image_count < start_id:
            image_count += 1
            continue

        image_info = image_list[image_count]
        print(image_count, image_info['_id'])
        image_count += 1

        img = Image.open(dataset_path + image_info['_id'] + '.jpg')

        try:
            diagnosis = image_info['meta']['clinical']['diagnosis']
        except KeyError:
            continue

        if diagnosis not in ['melanoma', 'nevus', 'seborrheic keratosis']:
            continue

        file = open(downsample_path + '256/' + image_info['_id'] + '.txt', 'w')
        file.write(diagnosis + '\n')

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

        new_width = 100
        new_height = round(img.size[1] * 1.0 * new_width / img.size[0])
        img = img.resize(size=(new_width, new_height), resample=Image.BICUBIC)
        pixels_mat = img.load()
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                file.write(str(x) + ' ' + str(y) + ' ')
                for k in range(3):
                    file.write(str(pixels_mat[x,y][k]) + ' ')
                file.write('\n')
        file.close()


if __name__ == '__main__':
    dataset_name = 'MSK-2'

    print('Downsample Images.', dataset_name)
    DownsampleImage(dataset_name=dataset_name)
    print('Finished.')