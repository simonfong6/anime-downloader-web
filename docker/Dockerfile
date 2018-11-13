FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y python3.5 \
                       python3-pip
RUN apt-get install -y git

RUN pip3 install flask flask-cors

RUN pip3 install anime-downloader[cloudflare]

RUN git clone https://github.com/simonfong6/anime-downloader-web