FROM public.ecr.aws/docker/library/python:latest

ARG PASSWORD

RUN echo root:${PASSWORD} | chpasswd
RUN apt-get update && apt-get install -y openssh-server sqlite3 curl
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN service ssh start

WORKDIR /ctf/pasta/

COPY src/ src/
COPY requirements.txt .
COPY start.sh .

RUN pip install -r requirements.txt
RUN touch flag.txt
RUN python3 src/initdb.py deomkicer_number_1_fans ${PASSWORD}

RUN chmod +x start.sh
CMD ./start.sh

# docker build --build-arg "PASSWORD=123" -t pasta .