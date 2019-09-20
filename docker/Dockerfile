FROM debian:buster-slim

RUN apt update && apt install python3-pip libjemalloc2 -y && apt-get clean

WORKDIR /root/sberbank/
COPY ./sberbank/ /root/sberbank/
RUN pip3 install -r requirements.txt
COPY entry.sh /root/sberbank/entry.sh

RUN chmod ugo+rwx /root/sberbank/entry.sh

ENV LD_PRELOAD='libjemalloc.so.2'

EXPOSE 8080

ENTRYPOINT ["/root/sberbank/entry.sh"]
