FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt-get install default-jre -y

COPY . /app
WORKDIR /app

RUN \
pip3 install bs4 && \
pip3 install requests && \
pip3 install numpy && \
pip3 install nltk && \
pip3 install tensorflow && \
pip3 install flask && \
python3 -m nltk.downloader punkt && \
python3 -m nltk.downloader averaged_perceptron_tagger && \
python3 -m nltk.downloader maxent_ne_chunker && \
python3 -m nltk.downloader wordnet && \
python3 -m nltk.downloader words 

CMD [ "python3", "FoodKG.py" ]