# run sshd
/usr/sbin/sshd -D &
# run the command
cd src
uvicorn app:app --host 0.0.0.0 --port 8000