FROM public.ecr.aws/docker/library/python:3.11-slim-buster@sha256:a201e091d3e0ccf42319402822b16d23cbcd74ff0576d51622a5e88f63fc85ac

ARG PASSWORD

WORKDIR /opt

RUN apt-get update
RUN apt-get install -y nano openssh-server \
    gcc curl

RUN echo root:${PASSWORD} | chpasswd
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN service ssh start

COPY src/ .
RUN touch /flag.txt

RUN pip install -r requirements.txt
RUN chmod +x ./start.sh

EXPOSE 8000
EXPOSE 22

CMD ./start.sh
