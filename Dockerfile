FROM pypy:3-5
ADD . .
RUN pip install -r requirements.txt
CMD [ "pypy3", "./server.py" ]
