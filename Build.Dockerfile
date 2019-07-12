FROM centos:6.10

RUN yum -y update && \
    yum -y install yum-utils && \
    yum -y groupinstall development && \
    yum -y install https://centos6.iuscommunity.org/ius-release.rpm && \
    yum -y install python36u && \
    yum -y install python36u-devel && \ 
    yum -y install python36u-setuptools

RUN easy_install-3.6 pip && \
    pip3 install pyinstaller

RUN mkdir -p Build/
WORKDIR Build/
ENV PYTHONPATH=/Build/scripts/
COPY scripts/ /Build/scripts/
RUN pip3 install -r scripts/requirements.txt
RUN pyinstaller scripts/switchboard.py -w --onefile 
RUN tar -czvf switchboard.tar -C /Build/dist/ .
# RUN pip3 install -r scripts/requirements.txt
# RUN pyinstaller scripts/switchboard.py -w --onefile
# RUN tar -czvf switchboard.tar -C dist/ .