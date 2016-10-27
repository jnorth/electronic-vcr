FROM python:latest
MAINTAINER Joseph North <north@sublink.ca>

RUN \
  apt-get update && \
  apt-get install -y libav-tools atomicparsley rtmpdump && \
  rm -rf /var/lib/apt/lists/* && \
  pip install youtube-dl

VOLUME /data
WORKDIR /data
COPY /electronic-vcr.py /app/

ENTRYPOINT ["python", "/app/electronic-vcr.py"]
CMD ["--script-path", "/data/vcr.json", "--data-path", "/data", "--interval", "12h0m0s"]
