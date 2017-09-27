FROM centos:latest
COPY ./ibd.py /usr/bin/ibd.py
RUN chmod +x /usr/bin/ibd.py
RUN echo "export TERM=xterm" >> /root/.bashrc
ENTRYPOINT ["/usr/bin/ibd.py"]
