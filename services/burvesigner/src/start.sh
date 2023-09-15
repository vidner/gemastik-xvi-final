#!/bin/bash

/usr/sbin/sshd -D &
chmod +x ./main.py
./main.py
