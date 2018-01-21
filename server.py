from flask import Flask,request,send_file,Response
from io import BytesIO
from PIL import Image
import logging
import time
import sys
import os

# Flask App
app = application = Flask(__name__)

# For very large images
Image.MAX_IMAGE_PIXELS = 100000000000
# Allowed image types
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Logger
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.debug("logging started")
logger = logging.getLogger(__name__)

# Resize 
def resize(size,image_content,mime_type):
    width=int(size.split('x')[0])
    height=int(size.split('x')[1])
    img = Image.open(image_content)
    if width and height:
        img = img.resize((width, height), Image.ANTIALIAS)
    elif not height:
        wpercent = (width / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width, hsize), Image.ANTIALIAS)
    elif not width:
        hpercent = (height / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(hpercent)))
        img = img.resize((wsize, height), Image.ANTIALIAS)
    tmp_img = BytesIO()
    img.save(tmp_img,mime_type)
    return tmp_img

# Routes
@app.route('/resize', methods=['POST'])
def resize_route():    
    logging.info("Got a new image. Time = %d",int(time.time()))
    start_time=int(time.time())
    # Get file object
    image_io = BytesIO()
    image_file = request.files['file']
    image_type = image_file.filename.rsplit('.', 1)[1].lower()
    if image_type not in ALLOWED_EXTENSIONS:
        return "Image Type Not Allowed",400
    # Because Image.save takes jpeg instead of jpg
    if image_type == "jpg": image_type="jpeg"
    image_file.save(image_io)
    # Size
    size=request.args.get('size')
    resized_image = resize(size=size,image_content=image_io,mime_type=image_type)
    resized_image.seek(0)
    logging.info("Finished resizing. Time needed= %d",int(time.time())-start_time)
    if image_type == "jpeg": image_type="jpg"
    return send_file(
                resized_image,
                attachment_filename='resized.png',
                mimetype='image/%s' %image_type
            )
# Main
if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=3000,
    )