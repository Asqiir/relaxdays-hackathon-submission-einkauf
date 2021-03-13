FROM python:3.9
WORKDIR /app
ADD . /app
RUN python3 -m pip install bottle
RUN python3 -m pip install 'bottle-swagger==1.2.0'
EXPOSE 8080
CMD ["python3","server.py"]
