FROM public.ecr.aws/docker/library/ubuntu:20.04

ARG PASSWORD

ENV DEBIAN_FRONTEND noninteractive

RUN echo root:${PASSWORD} | chpasswd
RUN apt-get update && apt-get install -y openssh-server lib32z1 xinetd cmake gcc curl
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN service ssh start

RUN useradd -m ctf

WORKDIR /ctf

RUN echo "Connection blocked" > /etc/banner_fail
COPY ctf.xinetd /etc/xinetd.d/ctf
COPY ./src/main.c ./
COPY ./start.sh ./
RUN gcc /ctf/main.c -no-pie -fno-stack-protector -Wl,-z,relro,-z,now -o /ctf/main
RUN touch /flag.txt
RUN chmod -R 755 /ctf
RUN chmod +x /ctf/start.sh

ENTRYPOINT []
CMD ["/usr/sbin/xinetd", "-dontfork"]

EXPOSE 8000