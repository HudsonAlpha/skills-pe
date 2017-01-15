# Very simple docker service to output the time every 10 seconds

FROM centos:7
MAINTAINER "Chris King" <tchrisking@gmail.com>

COPY datetime /usr/local/bin/datetime
RUN chmod +x /usr/local/bin/datetime

CMD ["/usr/local/bin/datetime"]
