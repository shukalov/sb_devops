#!/bin/bash

exec 2>> /root/sberbank/tmp/service.log
exec 1>> /root/sberbank/tmp/service.log

cd /root/sberbank/ && python3 service.py
