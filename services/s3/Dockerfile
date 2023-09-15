FROM public.ecr.aws/docker/library/python:3.11-slim-buster

ARG PASSWORD

WORKDIR /opt

RUN apt-get update
RUN apt-get install -y nano openssh-server curl

RUN echo root:${PASSWORD} | chpasswd
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN service ssh start

COPY src/ .

RUN mkdir -p uploads/
RUN pip install -r requirements.txt
RUN chmod +x ./start.sh

EXPOSE 80
EXPOSE 22

CMD ./start.sh
