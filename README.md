# Image Resizing Server
[![Build Status](https://travis-ci.org/OsamaJBR/python-img-resizing-server.svg?branch=master)](https://travis-ci.org/OsamaJBR/python-img-resizing-server) 

## Build & Run
```bash
$ docker build -f Dockerfile -t image-resizer .
$ docker run -p5000:5000 -it image-resizer
```

## Test it
```bash
$ curl -XGET 'https://img-resizer-srv.herokuapp.com/resize?url=https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg&size=500x500' 
```

## Params
```
use_default = 0 return error code if anything wrong happens.
            = 1 return no-image.png resized ( =1 is the default value)

size        = widthxheight, integers only

crop        = 0 resize the image without croping it
            = 1 crop the image if aspect ratio of new size is not as the original (defaul)

crop_type   = middle (default)
            = top
            = bottom

force_jpg   = 0 reserve the type of the image
            = 1 change the type to jpg

image_url   = url of the source image ( domain should be listed in allowed_domains in server.py file)
```
