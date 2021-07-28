FROM python:3.9.6
ADD . /ladeinorge-selenium
WORKDIR /ladeinorge-selenium
RUN pip install -r requirements.txt