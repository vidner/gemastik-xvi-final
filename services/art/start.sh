# run sshd
/usr/sbin/sshd -D &
# run the command
su ctf -c "bundle install"
su ctf -c "ruby /ctf/art/app.rb"