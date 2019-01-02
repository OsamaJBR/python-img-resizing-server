# Image Resizing Server

### Build & Run
```
$ docker build -f Dockerfile -t image-resizer .
$ docker run -p5000:5000 -it image-resizer
```

### Test it
```
$ curl -XGET 'http://localhost:3000/resize?url=https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg&size=500x500' 
```

### PARAMS
```
use_default = 0 return error code if anything wrong happens.
            = 1 return default image for arabiaweather ( =1 is the default value)

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
