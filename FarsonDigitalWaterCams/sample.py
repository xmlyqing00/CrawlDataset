import os
from shutil import copy2

def sample_images(image_folder, sample_folder, sample_n):

    sub_folders = os.listdir(image_folder)
    print(sub_folders)

    for sub_folder in sub_folders:

        video_path = os.path.join(image_folder, sub_folder)
        out_path = os.path.join(sample_folder, sub_folder)
        
        if not os.path.exists(out_path):
            os.makedirs(out_path)

        image_list = os.listdir(video_path)
        image_list.sort(key = lambda x: (len(x), x))
        image_n = len(image_list)
        step = image_n / sample_n
        idx = 0

        for i in range(sample_n):
            round_idx = min(round(idx), image_n - 1)
            image_path = os.path.join(video_path, image_list[round_idx])
            print(image_path)
            copy2(image_path, out_path)
            idx += step

if __name__ == '__main__':

    image_folder = '/Ship01/Dataset/water/FarsonWater'
    sample_folder = '/Ship01/Dataset/water/FarsonWater_sample'
    sample_n = 20

    sample_images(image_folder, sample_folder, sample_n)