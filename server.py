from flask import Flask,request,send_file,jsonify
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
from configparser import SafeConfigParser
import requests
import hashlib
import time
import sys
import re
import os

# Flask App
app = application = Flask(__name__)

# Config
config = SafeConfigParser()
config.read("config.ini")
allowed_extensions = config.get('resizer','allowed_types').split(',')
allowed_domains = config.get('resizer','allowed_domains').split(',')

# For very large images
Image.MAX_IMAGE_PIXELS = 10000000

# Functions
def get_filename_from_cd(cd):
    '''
    Get filename from content-disposition
    '''
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

def get_domain_from_url(url):
    parsed = urlparse(url)
    hostname = parsed.netloc.split(':')[0]
    parts = hostname.split('.')
    return parts[-2] + '.' + parts[-1]

def is_downloadable(url):
    '''
    Does the url contain a downloadable resource
    '''
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

# Resize
def resize_and_crop(image_content, size, crop_type='middle'):
    # If height is higher we resize vertically, if not we resize horizontally
    img = Image.open(image_content).convert('RGB')
    # Get current and desired ratio for the images
    current_img_ratio = img.size[0] / float(img.size[1])
    if not size[1]:
        size[1] = int(size[0] * (1/current_img_ratio))
    if not size[0]:
        size[0] = int(size[1] * current_img_ratio)
    desired_ratio = size[0] / float(size[1])
    #The image is scaled/cropped vertically or horizontally depending on the ratio
    if desired_ratio > current_img_ratio:
        img = img.resize((size[0], int(size[0] * img.size[1] / img.size[0])),Image.ANTIALIAS)
        if crop_type == 'top':
            box = (0, 0, img.size[0], size[1])
        elif crop_type == 'middle':
            box = (0, (img.size[1] - size[1]) / 2, img.size[0], (img.size[1] + size[1]) / 2)
        elif crop_type == 'bottom':
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        img = img.crop(box)
    elif desired_ratio < current_img_ratio:
        img = img.resize((int(size[1] * img.size[0] / img.size[1]), size[1]),Image.ANTIALIAS)
        if crop_type == 'top':
            box = (0, 0, size[0], img.size[1])
        elif crop_type == 'middle':
            box = ((img.size[0] - size[0]) / 2, 0, (img.size[0] + size[0]) / 2, img.size[1])
        elif crop_type == 'bottom':
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        img = img.crop(box)
    else :
        img = img.resize((size[0], size[1]),Image.ANTIALIAS)
    return img
    
def resize(size,image_content):
    img = Image.open(image_content).convert('RGB')
    if size[0] and size[1]:
        img = img.resize((size[0], size[1]), Image.ANTIALIAS)
    elif not size[1]:
        wpercent = (size[0] / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((size[0], hsize), Image.ANTIALIAS)
    elif not size[0]:
        hpercent = (size[1] / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, size[1]), Image.ANTIALIAS)
    return img

# Routes
@app.route('/resize', methods=['POST','GET'])
def resize_route():
    use_default =int(request.args.get('use_default',1))    
    size=request.args.get('size','300x300')
    crop_type=request.args.get('crop_type','middle')
    crop = int(request.args.get('crop',1))
    force_jpg = int(request.args.get('force_jpg', 0))    
    image_url = request.args.get('url')
    
    if not image_url:
        return jsonify({'error' : 'missing param \'url\''}),400
    
    if not is_downloadable(image_url) and not use_default:
        return jsonify({'error' : 'url does not have downloadable media'}),400
    
    if get_domain_from_url(image_url) not in allowed_domains:
        return jsonify({'error' : 'only images from allowed soruce should be used.'}),400

    response = requests.get(image_url,stream=True,allow_redirects=True)
    image = b'' 
    
    if response.status_code != 200 and not use_default:
        return jsonify({'error' : 'wrong url'}),400
    elif response.status_code != 200 and use_default:
        with open(config.get('resizer','no_image_path'), 'rb') as defaultImage:
            image = defaultImage.read()
        content_type = 'image/jpeg'
    else:
        image = response.content
        content_type = response.headers['Content-Type']

    if 'image' in content_type:
        image_type = content_type.split('/')[1]
    else:
        return jsonify({'error' : 'url does not have content type: image/*'}),400
    
    if force_jpg and image_type not in ['gif']: image_type = 'jpeg'
    
    with BytesIO(image) as fp:
        desired_size = []
        desired_size.append(int(size.split("x")[0]))
        desired_size.append(int(size.split("x")[1]))
        if crop:
            resized_image = resize_and_crop(size=desired_size,image_content=fp,crop_type=crop_type)
        else:
            resized_image = resize(size=desired_size,image_content=fp)
        img = BytesIO()
        print(image_type)
        resized_image.save(img,format=image_type,quality=85)
        img.seek(0)
        return send_file(
                img,
                mimetype=content_type
            )
# Main
if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )
