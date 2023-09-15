#!/bin/sh
/usr/sbin/sshd -D &
su ctf -c "/ctf/main"