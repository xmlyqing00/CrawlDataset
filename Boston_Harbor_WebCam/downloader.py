import os
import time
import cv2
import numpy as np
from urllib import request
from PIL import ImageFont, ImageDraw, Image
from datetime import datetime
import pytz 


def process(imageurl, folder, name):
    if not os.path.exists(folder + '/' + name):
        os.makedirs(folder + '/' + name)
        
    try:
        # req = request.Request(imageurl, headers=base_headers, method='GET')
        # stream = request.urlopen(req)
        # data = ''
        # while True:
        #     data += str(stream.read(1024))
        #     jpeg_st = data.find('\xff\xd8')
        #     jpeg_ed = data.find('\xff\xd9')

        #     print(jpeg_st, jpeg_ed)

        #     if jpeg_st != -1 and jpeg_ed != -1:
        #         img_data = data[jpeg_st: jpeg_ed+2]
        #         data = data[jpeg_ed+2:]

        #         img = cv2.imdecode(np.fromstring(img_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        #         break

        cap = cv2.VideoCapture(imageurl)

        now_time = datetime.now(pytz.timezone(timezone))
        imageName = now_time.strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
        filepath = os.path.join(folder + '/' + name + '/' + imageName)

        res, img = cap.read()
        cv2.imwrite(filepath, img)
        # image = open(filepath, 'wb')
        # image.write(data)
        # image.close()
        
        # add timestamp to images
        font = ImageFont.truetype('Roboto-Regular.ttf', 28)
        img = cv2.imread(filepath)
        height, width, c = img.shape
        pos = (50, height-50)
        cv2_im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im_rgb)
        draw = ImageDraw.Draw(pil_im)
        draw.text(pos, imageName[:-4] + ' ' + timezone, font = font)
        cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        cv2.imwrite(filepath, cv2_im_processed)
        cap.release()
        return imageName

    except Exception as ex_results:
        print ('Error: ', ex_results)

        

if __name__ == '__main__':
    rootfolder = '/Ship01/Dataset/water_collection/'
    interval = 1
    totalTime = 180
    timezone = 'America/New_York'
    base_headers = {
        # 'Connection': 'keep-alive',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    c2 = {
        'url': 'http://108.49.186.56/axis-cgi/mjpg/video.cgi?resolution=1024x768&dummy=1510881269401',
        'name': 'Boston_Tea_Party_Museum_Webcam_2_202006'
    }
        
    if not os.path.exists(os.path.join(rootfolder, c2['name'])):
        os.makedirs(os.path.join(rootfolder, c2['name']))
    
    total = int(totalTime*60/interval)
    for gap in range (total):
        # process('http://108.49.186.55/jpg/1/image.jpg', rootfolder, 'boston_harbor_0_202006')
        # process('http://108.49.186.56/jpg/1/image.jpg', rootfolder, 'boston_harbor_1_202006')
        # process('http://108.49.186.55/axis-cgi/mjpg/video.cgi?resolution=1024x768&dummy=1592412129560', rootfolder, 'Boston_Tea_Party_Museum_Webcam_1_202006')
        img_name = process(c2['url'], rootfolder, c2['name'])
        print(f'{gap} / {total}', f'Downloaded {img_name}')

        time.sleep(interval*60)
    
