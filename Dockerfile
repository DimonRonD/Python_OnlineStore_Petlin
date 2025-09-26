FROM ubuntu:latest
LABEL authors="dmitriipetlin"

ENTRYPOINT ["top", "-b"]