FROM python:3.5-alpine
MAINTAINER jbr.osama@gmail.com

ADD . .
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN apk add linux-headers
RUN pip install -r requirements.txt

EXPOSE 3000
CMD [ "uwsgi", "-i","./uwsgi.ini","--http-socket","0.0.0.0:3000","--wsgi-disable-file-wrapper"]
