FROM public.ecr.aws/docker/library/python:3.11-slim-buster

ARG PASSWORD

WORKDIR /opt

RUN apt-get update
RUN apt-get install -y nano openssh-server \
    gcc python-dev python3-dev libgmp3-dev curl

RUN echo root:${PASSWORD} | chpasswd
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN service ssh start

COPY src/ .
RUN touch /flag.txt
RUN touch /priv.data

RUN pip install -r requirements.txt
RUN python3 database/init.py merricx_number_1_fans ${PASSWORD}
RUN chmod +x ./start.sh

EXPOSE 80
EXPOSE 22

CMD ./start.sh
