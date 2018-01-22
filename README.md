# Image Resizing Server

### Start the server
```
$ docker run -p3000:3000 -it --rm jbrosama/image-resizer
```
### Test it
```
$ curl -F 'file=@example.jpg' 'http://localhost:3000/resize?size=500x500' -o resized.jpg
```
