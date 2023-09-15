FROM public.ecr.aws/docker/library/python:3.10.6

ARG PASSWORD

RUN echo root:${PASSWORD} | chpasswd
RUN apt-get update && apt-get install -y openssh-server curl
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN service ssh start

RUN pip install --upgrade mongoengine blacksheep uvicorn passlib pycryptodome pytz urllib3 requests

WORKDIR /app

COPY ./src .
RUN touch /flag.txt

COPY ./start.sh .
RUN chmod +x /app/start.sh

CMD ./start.sh