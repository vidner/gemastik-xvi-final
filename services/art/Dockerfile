FROM public.ecr.aws/docker/library/ruby:2.7.2

ARG PASSWORD

RUN echo root:${PASSWORD} | chpasswd
RUN apt-get update && apt-get install -y openssh-server curl
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN service ssh start

WORKDIR /ctf/art/

RUN useradd -m ctf
RUN chown -R root:root /ctf/art/

COPY Gemfile .
COPY app.rb .
COPY start.sh .

RUN bundle install
RUN touch /flag.txt

RUN chmod +x start.sh
CMD ./start.sh