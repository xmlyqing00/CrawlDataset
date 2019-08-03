from datetime import datetime
from FarsonDigitalWaterCams.image_downloader import ImageDownloader
from FarsonDigitalWaterCams.riverlevel_downloader import RiverlevelDownloader

if __name__ == '__main__':

    loc_names = ['auldgirth', 'bewdley', 'cockermouth', 'evesham-lock', 'aberlour', 'keswick_greta', 'holmrook', 'worcester', 'galway-city', 'dublin']
    image_folder = '/Ship01/Dataset/water/FarsonWater'
    img_n = 200
    time_st = datetime(2019, 8, 3, 8, 0, 0) # London time
    interval = 180

    # image_downloader = ImageDownloader(loc_names, image_folder, img_n, time_st, interval)
    # image_downloader.batch_fetch_imgs()

    riverlevel_folder = '/Ship01/Dataset/water/FarsonWater_riverlevel'
    riverlevel_downloader = RiverlevelDownloader(loc_names, riverlevel_folder, img_n, time_st, interval)
    riverlevel_downloader.batch_fetch_riverlevels()