FROM ubuntu:19.10
RUN apt-get update && apt-get upgrade -y
WORKDIR /app
COPY . /app
RUN apt-get install build-essential python3-dev -y
RUN apt-get install python3-pip -y
RUN pip3 install Pillow
RUN pip3 install pymongo[srv]
RUN pip3 install -r requirements.txt
RUN pip3 install wheel
RUN pip3 install uwsgi
CMD ["python3", "run.py"]
