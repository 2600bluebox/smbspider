# consider something lighter, alpine?
FROM ubuntu:22.04

# labels for the smbspider img
LABEL maintainer="2600bluebox@gmail.com"
LABEL version="0.1"
LABEL description="Image for smbspider"

# update and upgrade the pkg repo
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt install -y less python3.10 python3-pip samba smbclient smbmap vim iputils-ping \
	&& ln -s /usr/bin/python3.10 /usr/bin/python
RUN apt clean

# setup shares on a separate user
RUN useradd -ms /bin/bash user
USER user

RUN mkdir /home/user/shares
RUN mkdir /home/user/smbspider

ADD ./shares /home/user/shares
ADD ./smbspider /home/user/smbspider

# python reqs
RUN pip install -r /home/user/smbspider/requirements.txt

# some samba setup
USER root
COPY ./shares/smb.conf /etc/samba/smb.conf

RUN chown -R user:user /home/user/shares
RUN chown -R user:user /home/user/smbspider

RUN chmod -R 755 /home/user/shares

RUN chmod +x /home/user
