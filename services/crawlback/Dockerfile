FROM public.ecr.aws/docker/library/php:8.0-apache

ARG PASSWORD

RUN echo root:${PASSWORD} | chpasswd
RUN apt-get update && apt-get install -y openssh-server curl
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN service ssh start

COPY src/ /var/www/html
RUN mkdir /var/www/html/backups
RUN chown -R www-data:www-data /var/www/html/backups
RUN chmod -R 777 /var/www/html/backups

RUN touch /flag.txt
COPY start.sh .

RUN chmod +x start.sh
CMD ./start.sh
