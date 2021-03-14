FROM python:3.9
WORKDIR /app
ADD . /app
RUN python3 -m pip install bottle
RUN python3 -m pip install pyyaml
RUN python3 -m pip install python-levenshtein
RUN python3 -m pip install matplotlib
RUN python3 -m pip install pathlib
EXPOSE 8080
CMD ["python3","server.py"]
