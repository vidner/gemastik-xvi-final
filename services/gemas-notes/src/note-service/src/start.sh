#!/bin/sh
/usr/sbin/sshd -D &

cd /app/src/ && ./run.sh